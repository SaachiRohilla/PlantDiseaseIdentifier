import os
import numpy as np
import json
import glob
from typing import List, Tuple

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR = os.path.join(BASE_DIR, 'vectorize_data')

SIZE = (224, 224)
BATCH = 10
EPOCHS = 20
AUTOTUNE = tf.data.AUTOTUNE

MODEL = os.path.join(BASE_DIR, 'model', 'plant_disease_cnn')

CLASSES = ["bac", "fung", "hea", "pes", "vir"]


def vector_files(classes: List[str], base_dir: str = DIR) -> Tuple[List[str], List[int]]:
    file_paths = []
    labels = []

    for label_id, class_name in enumerate(classes):
        vector_dir = os.path.join(base_dir, class_name)

        if not os.path.isdir(vector_dir):
            print(f"Warning: directory not found: {vector_dir}")
            continue

        npy_files = sorted(glob.glob(os.path.join(vector_dir, "*.npy")))

        for file_path in npy_files:
            file_paths.append(os.path.abspath(file_path))
            labels.append(label_id)

    return file_paths, labels

def file_loading(path):
    arr = np.load(path.decode("utf-8")).astype(np.float32)

    if arr.max() > 1.1:
        arr = arr / 255.0

    if arr.ndim == 2:
        arr = np.expand_dims(arr, -1)

    return arr

def fix_channels(x):
    if x.shape[-1] == 1:
        return np.repeat(x, 3, axis=-1)
    elif x.shape[-1] == 4:
        return x[..., :3]
    return x

def read_image(path):
    img = tf.numpy_function(file_loading, [path], tf.float32)
    img.set_shape([None, None, None])
    return img

def process_image(img):
    img = tf.numpy_function(lambda x: fix_channels(x), [img], tf.float32)
    img.set_shape([None, None, 3])

    img = tf.image.resize(img, SIZE)
    img = tf.clip_by_value(img, 0.0, 1.0)

    return img

def _read(path, label):
    img = read_image(path)
    img = process_image(img)
    return img, label

def make_dataset(file_paths, labels, batch_size=BATCH, shuffle=True):
    ds = tf.data.Dataset.from_tensor_slices((file_paths, labels))

    ds = ds.map(_read, num_parallel_calls=AUTOTUNE)

    if shuffle:
        ds = ds.shuffle(1024)

    ds = ds.batch(batch_size).prefetch(AUTOTUNE)

    return ds

def build_model(input_shape=(224, 224, 3), num_classes=5):
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )

    base_model.trainable = False

    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs * 255.0)

    x = base_model(x, training=False)

    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)

    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def main():
    os.makedirs(os.path.dirname(MODEL), exist_ok=True)

    tf.random.set_seed(42)
    np.random.seed(42)

    print("TF version:", tf.__version__)
    print("NumPy version:", np.__version__)

    file_paths, labels = vector_files(CLASSES)

    if len(file_paths) == 0:
        raise RuntimeError("No .npy files found. Check vectorize_data path.")

    print("Total samples:", len(file_paths))

    counts = {CLASSES[i]: labels.count(i) for i in range(len(CLASSES))}
    print("Class distribution:", counts)

    fp_train, fp_temp, y_train, y_temp = train_test_split(
        file_paths, labels,
        test_size=0.25,
        stratify=labels,
        random_state=42
    )

    fp_val, fp_test, y_val, y_test = train_test_split(
        fp_temp, y_temp,
        test_size=0.5,
        stratify=y_temp,
        random_state=42
    )

    print(f"Train: {len(fp_train)}, Val: {len(fp_val)}, Test: {len(fp_test)}")

    train_ds = make_dataset(fp_train, y_train, shuffle=True)
    val_ds = make_dataset(fp_val, y_val, shuffle=False)
    test_ds = make_dataset(fp_test, y_test, shuffle=False)

    model = build_model(
        input_shape=(SIZE[0], SIZE[1], 3),
        num_classes=len(CLASSES)
    )

    model.summary()
    ckpt = tf.keras.callbacks.ModelCheckpoint(
        MODEL + ".keras",
        save_best_only=True,
        monitor="val_accuracy",
        mode="max"
    )

    early = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=6,
        restore_best_weights=True
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[ckpt, early]
    )

    model.evaluate(test_ds)

    y_true, y_pred = [], []

    for x, y in test_ds:
        preds = model.predict(x, verbose=0)
        y_true.extend(y.numpy())
        y_pred.extend(np.argmax(preds, axis=1))

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=CLASSES))

    # =========================
    # SAVE MODEL
    # =========================
    model.save(MODEL + ".keras", include_optimizer=False)

    with open(os.path.join(BASE_DIR, "model", "label_map.json"), "w") as f:
        json.dump({"classes": CLASSES}, f)

    print("Saved model successfully!")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
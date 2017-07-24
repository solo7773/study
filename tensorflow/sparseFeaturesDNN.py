
import tensorflow as tf

sparse_feature_a = tf.contrib.layers.sparse_column_with_hash_bucket('col1', 3, dtype=tf.int32)
sparse_feature_b = tf.contrib.layers.sparse_column_with_hash_bucket('col2', 1000, dtype=tf.int32)

sparse_feature_a_emb = tf.contrib.layers.embedding_column(sparse_id_column=sparse_feature_a, dimension=2)
sparse_feature_b_emb = tf.contrib.layers.embedding_column(sparse_id_column=sparse_feature_b, dimension=2)
feature_c = tf.contrib.layers.real_valued_column('price')

estimator = tf.contrib.learn.DNNClassifier(
    feature_columns=[sparse_feature_a_emb, sparse_feature_b_emb, feature_c],
    hidden_units=[5, 3],
    n_classes=2,
    model_dir='./tfTmp/tfTmp0')

# Input builders
def input_fn_train(): # returns x, y (where y represents label's class index).
    features = {'col1': tf.SparseTensor(indices=[[0, 1], [0, 5], [0, 7], [0, 9]],
                                      values=[1, 2, 1, 3],
                                      dense_shape=[3, int(250e6)]),
    'col2': tf.SparseTensor(indices=[[0, 2], [0, 3]],
                                        values=[4, 5],
                                        dense_shape=[3, int(100e6)]),
                            'price': tf.constant([5.2, 0, 0])}
    labels = tf.constant([0, 1, 1])
    return features, labels

estimator.fit(input_fn=input_fn_train, steps=100)

def input_fn_eval(): # returns x, y (where y represents label's class index).
  pass
#estimator.evaluate(input_fn=input_fn_eval)
def input_fn_predict(): # returns x, None
    features = {'col1': tf.SparseTensor(indices=[[0, 1], [0, 5], [0, 9], [0, 7]],
                                      values=[1, 2, 1, 0],
                                      dense_shape=[1, int(250e6)]),
    'col2': tf.SparseTensor(indices=[[0, 2], [0, 3]],
                                        values=[4, 5],
                                        dense_shape=[1, int(100e6)]),
                            'price': tf.constant([4.2])}
    return features
# predict_classes returns class indices.
prediction = estimator.predict_classes(input_fn=input_fn_predict)
print(list(prediction))

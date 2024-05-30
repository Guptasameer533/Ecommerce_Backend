# cython: language_level=3, boundscheck=False, wraparound=False

import numpy as np
cimport numpy as np

def recommend_products(user_id, num_recommendations=5):
    cdef int[:] user_products = user_product_matrix.loc[user_id, :].values
    cdef int[:, :] matrix_values = user_product_matrix.values
    cdef double[:, :] user_similarity_scores = np.zeros((matrix_values.shape[0], 1), dtype=np.double)

    # Compute the cosine similarity between the user and other users
    for i in range(matrix_values.shape[0]):
        user_similarity_scores[i, 0] = cosine_similarity(matrix_values[i, :].reshape(1, -1), user_products.reshape(1, -1))

    # Get the top similar users (excluding the user themselves)
    cdef int[:] top_similar_users = np.argsort(user_similarity_scores.flatten())[-num_recommendations-1:-1][::-1]

    # Get the products purchased by the top similar users
    cdef int[:] top_user_products = np.sum(matrix_values[top_similar_users, :], axis=0)

    # Exclude products already purchased by the user
    cdef int[:] recommended_products = np.array([i for i in top_user_products if i not in user_products])

    return recommended_products.tolist()
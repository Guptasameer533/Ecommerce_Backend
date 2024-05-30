import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load user-product interaction data (dummy data for this example)
interactions = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3, 3, 3],
    'product_id': [1, 2, 2, 3, 1, 3, 4]
})

# Create a user-product matrix
user_product_matrix = interactions.pivot_table(index='user_id', columns='product_id', values='product_id', fill_value=0)

# Calculate the cosine similarity between users
user_similarity = cosine_similarity(user_product_matrix.T)

def recommend_products(user_id, num_recommendations=5):
    # Get the user's purchased products
    user_products = user_product_matrix.loc[user_id, :].values.reshape(1, -1)

    # Calculate the similarity between the user and other users
    user_similarity_scores = cosine_similarity(user_product_matrix.values, user_products).flatten()

    # Get the top similar users (excluding the user themselves)
    top_similar_users = user_similarity_scores.argsort()[-num_recommendations-1:-1][::-1]

    # Get the products purchased by the top similar users
    top_user_products = user_product_matrix.iloc[top_similar_users, :].sum().sort_values(ascending=False)

    # Exclude products already purchased by the user
    recommended_products = top_user_products[~top_user_products.index.isin(user_products.flatten())].index.tolist()

    return recommended_products
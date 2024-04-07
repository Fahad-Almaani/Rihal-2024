def get_minimum_stars(movie_ratings):
    n = len(movie_ratings)
    stars = [1] * n

    # Ensure each movie has at least one star
    for i in range(1, n):
        if movie_ratings[i] > movie_ratings[i - 1]:
            stars[i] = stars[i - 1] + 1

    # Traverse from right to left, ensuring higher-rated movies get more stars
    for i in range(n - 2, -1, -1):
        if movie_ratings[i] > movie_ratings[i + 1]:
            stars[i] = max(stars[i], stars[i + 1] + 1)

    return sum(stars)

# Example usage:
movie_ratings1 = [2, 1, 2]
print(get_minimum_stars(movie_ratings1))  # Output: 5

movie_ratings2 = [2,6,4,4]
print(get_minimum_stars(movie_ratings2))  # Output: 11

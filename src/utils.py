"""
Script for utility functions.
"""
# Modules
import pandas


def clean_listings(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Cleaning listings data.

    Args:
        df: Listings data.

    Returns:
        Listings cleaned.
    """
    # Parameters
    index = [
        'id',
    ]
    numcols = [
        'host_response_rate',
        'host_acceptance_rate',
        'host_listings_count',
        'accommodates',
        'bathrooms',
        'bedrooms',
        'beds',
        'price',
        'security_deposit',
        'cleaning_fee',
        'guests_included',
        'extra_people',
        'number_of_reviews',
        'review_scores_rating',
        'review_scores_accuracy',
        'review_scores_cleanliness',
        'review_scores_checkin',
        'review_scores_communication',
        'review_scores_location',
        'review_scores_value',
    ]
    boolcols = [
        'host_is_superhost',
        'host_identity_verified',
    ]
    catcols = [
        'host_response_time',
        'neighbourhood',
        'property_type',
        'room_type',
        'bed_type',
        'cancellation_policy',
    ]
    # Setting index
    df = df.set_index(index)

    # Dropping columns
    df = df.drop(
        columns=[col for col in df.columns if col not in numcols+catcols+boolcols]
    )

    # Converting datatypes
    for col in numcols:
        if col in df.select_dtypes(object):
            df[col] = df[col].astype(str).str.replace('[%$,. ]', '', regex=True).astype(float)
        elif col in df.select_dtypes(int):
            df[col] = df[col].astype(float)
    for col in boolcols:
         df[col] = df[col].astype(str).replace('t', '1').replace('f', '0').astype(float)

    return df
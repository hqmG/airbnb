"""
Function script for processing data.
"""
# Modules
import pandas
import re
from typing import Tuple


def clean_calendar(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Cleaning calendar data.

    Args:
        df: Calendar data.

    Returns:
        Calendar cleaned.
    """
    # Parameters
    floatcols = [
        'price',
    ]
    boolcols = [
        'available',
    ]
    datecols = [
        'date',
    ]

    # Converting datatypes
    for col in floatcols:
        df[col] = df[col].astype(str).str.replace('[%$,. ]', '', regex=True).astype(float)
    for col in boolcols:
        df[col] = df[col].astype(str).replace('t', '1').replace('f', '0').astype(float)
    for col in datecols:
        df[col] = pandas.to_datetime(df[col])
    return df


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
    df = df.drop(columns=[col for col in df.columns if col not in numcols + catcols + boolcols])

    # Converting datatypes
    for col in numcols:
        if col in df.select_dtypes(object):
            df[col] = df[col].astype(str).str.replace('[%$,. ]', '', regex=True).astype(float)
        elif col in df.select_dtypes(int):
            df[col] = df[col].astype(float)
    for col in boolcols:
        df[col] = df[col].astype(str).replace('t', '1').replace('f', '0').astype(float)
    return df


def clean_reviews(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Cleaning reviews data.

    Args:
        df: Reviews data.

    Returns:
        Reviews cleaned.
    """
    # Parameters
    index = [
        'id',
    ]
    datecols = [
        'date',
    ]

    # Setting index
    df = df.set_index(index)

    # Converting datatypes
    for col in datecols:
        df[col] = pandas.to_datetime(df[col])
    return df


def process(
    data: pandas.DataFrame,
) -> Tuple[pandas.DataFrame]:
    """
    Processing data.

    Args:
        data: Data to process.

    Returns:
        Features and targets.
    """
    # Parameters
    numcols1 = [
        'accommodates',
        'bathrooms',
        'bedrooms',
        'beds',
        'security_deposit',
        'cleaning_fee',
        'guests_included',
        'extra_people',
        'number_of_reviews',
    ]
    numcols2 = [
        'host_response_rate',
        'host_acceptance_rate',
        'host_listings_count',
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
    target = [
        'price',
    ]

    # Processing
    for col in data.columns:

        # Numerical columns: Imputing missing values with zero
        if col in numcols1:
            data[col] = data[col].fillna(0.0)

        # Numerical columns: Adding NaN column and imputing missing values with mean
        elif col in numcols2:
            dummy = pandas.get_dummies(
                data=data[col],
                prefix=col,
                prefix_sep='__',
                dummy_na=True,
                dtype=float,
            )[[f'{col}__nan']]
            data = pandas.concat([data.drop(col, axis=1), data[col], dummy], axis=1)
            data[col] = data[col].fillna(data[col].mean())

        # Boolean columns: Adding indicator and NaN columns
        elif col in boolcols:
            dummies = pandas.get_dummies(
                data=data[col],
                prefix=col,
                prefix_sep='__',
                dummy_na=True,
                drop_first=True,
                dtype=float,
            )
            dummies = dummies.rename(columns={col: col.replace('1.0', 'true') for col in dummies.columns})
            data = pandas.concat([data.drop(col, axis=1), dummies], axis=1)

        # Categorical columns: Adding indicator and NaN columns
        elif col in catcols:
            dummies = pandas.get_dummies(
                data=data[col],
                prefix=col,
                prefix_sep='__',
                dummy_na=True,
                drop_first=False,
                dtype=float,
            )
            dummies = dummies.rename(columns={col: re.sub('[-/ ]', '_', col).lower() for col in dummies.columns})
            data = pandas.concat([data.drop(col, axis=1), dummies], axis=1)

    # Features and targets
    X = data.drop(columns=target)
    y = data[target]
    return X, y

"""
User Classification Module - Handles classification of user counts into categories

This module provides functionality to classify raw user count numbers into
meaningful milestone categories that can be used for reporting, filtering,
and analysis. It offers two classification schemes:

1. Standard Classification:
   - 0-10k users
   - 10-20k users
   - 20-30k users
   - 30-40k users
   - >40k users

2. Detailed Classification:
   - 0-10k users
   - 10-20k users
   - 20-30k users
   - 30-40k users
   - 40k-100k users
   - >100k users

These classifications help transform raw analytics numbers into more
meaningful categories for content performance evaluation.
"""

def classify_users(users, detailed=False):
    """
    Classify user counts into milestone categories.
    
    This function takes a raw user count number and assigns it to a predefined
    milestone category. These categories make it easier to understand content 
    performance at a glance and group content by performance tiers.
    
    Args:
        users (int): Number of users to classify
        detailed (bool): Whether to use more detailed classification buckets.
            When True, adds an additional '40k-100k' category and changes the
            top category to '>100k' instead of '>40k'.
        
    Returns:
        str: Classification category (e.g., "0-10k", "10-20k", etc.)
        
    Examples:
        >>> classify_users(5000)
        '0-10k'
        >>> classify_users(25000)
        '20-30k'
        >>> classify_users(45000)
        '>40k'
        >>> classify_users(45000, detailed=True)
        '40k-100k'
    """
    if users < 10000:
        return "0-10k"
    elif users < 20000:
        return "10-20k"  
    elif users < 30000:
        return "20-30k"
    elif users < 40000:
        return "30-40k"
    elif detailed and users < 100000:
        return "40k-100k"
    else:
        return ">40k" if not detailed else ">100k"

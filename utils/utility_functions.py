from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from utils.constant import *
import time
import os
from datetime import date


def custom_response(status, data={}, error=True, message="", is_pagination=False):
    if not is_pagination:
        return Response(
            {
                CUSTOM_RESPONSE_STATUS_CODE: status,
                CUSTOM_RESPONSE_ERROR: error,
                CUSTOM_RESPONSE_DATA: data,
                CUSTOM_RESPONSE_MESSAGE: message,
            },
            status=status,
        )
    return Response(
        {
            CUSTOM_RESPONSE_STATUS_CODE: status,
            CUSTOM_RESPONSE_ERROR: error,
            **data,
            CUSTOM_RESPONSE_MESSAGE: message,
        },
        status=status,
    )


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for controlling pagination behavior.

    Inherits from PageNumberPagination provided by Django REST Framework.
    """

    page_size = 10  # Default page size for pagination
    page_size_query_param = "page_size"  # Query parameter name for specifying page size
    max_page_size = 999  # Maximum page size allowed for pagination

    def get_paginated_response(self, data):
        """
        Customizes the paginated response format.

        Args:
            data (list): List of serialized data to be paginated.

        Returns:
            dict: A dictionary containing pagination metadata and paginated data.
        """
        return {
            "links": {
                "next": self.get_next_link(),  # Link to the next page
                "previous": self.get_previous_link(),  # Link to the previous page
            },
            "count": self.page.paginator.count,  # Total count of items across all pages
            CUSTOM_RESPONSE_DATA: data,  # Paginated data for the current page
        }


def custom_pagination(get_page_size, queryset, request, serializer_class, context={}):
    """
    Customizes pagination for a queryset based on parameters.

    Args:
        get_page_size (int): The page size requested by the client.
        queryset (QuerySet): The queryset to be paginated.
        request (HttpRequest): The HTTP request object.
        serializer_class (Serializer): The serializer class used for serializing queryset data.
        context (dict, optional): Additional context to pass to the serializer. Defaults to {}.

    Returns:
        Response: Paginated response containing serialized data.
    """
    pagination_class = CustomPagination  # Using CustomPagination class for pagination

    if get_page_size:  # Checking if a specific page size is requested
        pagination_class.page_size = (
            get_page_size  # Setting the page size for pagination
        )

    paginator = (
        pagination_class()
    )  # Initializing the paginator with the specified pagination class

    # Paginating the queryset based on the request
    pagination_queryset = paginator.paginate_queryset(
        queryset=queryset, request=request
    )
    # Serializing the paginated queryset data
    serializer = serializer_class(pagination_queryset, context=context, many=True)
    # Getting the paginated response
    response = paginator.get_paginated_response(serializer.data)
    return response  # Returning the paginated response


def path_and_rename(instance, file_name):
    """
    Generates a unique file path and name based on the current date and time.

    Args:
        instance: The instance of the model to which the file is being attached.
        file_name (str): The original name of the file.

    Returns:
        str: The unique file path and name.
    """
    # Getting current time in a formatted string
    todays_time = time.strftime("%y%m%d_%H%M%S")
    base_name, extension = os.path.splitext(file_name)
    # Truncating the base name to 20 characters
    truncated_name = base_name[:20]
    characters_to_exclude = {WHITE_SPACE, "*", DOT}
    # Removing certain characters from the truncated name
    stripped_str = "".join(
        char for char in truncated_name if char not in characters_to_exclude
    )
    # Constructing the new file name with timestamp
    filename = stripped_str + SINGLE_UNDERSCORE + todays_time + extension
    # Constructing the final file path with date prefix
    return FILES_LOCATION_POST_MEDIA + "{}-{}-{}-{}".format(
        date.today().year, date.today().month, date.today().day, filename
    )

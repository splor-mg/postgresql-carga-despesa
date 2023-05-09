import numpy as np
import os
import pandas as pd

FRICT_TO_DTYPES = {
    'string': object
    ,
    'number': np.float64
    ,
    'integer': 'Int64'
    ,
    'boolean': bool
    ,
    'null': None
    ,
    'object': object
    ,
    'datetime': 'datetime64[ns]'
    ,
    'date': 'datetime64[ns]'
    ,
    'time': 'datetime64[ns]'
    ,
    'geopoint': object
    ,
    'geojson': object
    ,
    'any': object
}

def remove_path_redundancies(resource):
    path1 = os.path.normpath(resource.basepath).replace('\\','/')
    path2 = os.path.normpath(resource.path).replace('\\','/')
    path1_folders = path1.split('/')
    path2_folders = path2.split('/')
    common_folders = [folder for folder in path1_folders if folder in path2_folders]

    for folder in common_folders:
        path2_folders.remove(folder)

    new_path = os.path.normpath(os.path.join(path1, *path2_folders))

    return new_path


def dtypes_from_datapackage(resource, df):

    schema = resource.schema
    dtypes_dict = {field.name: FRICT_TO_DTYPES.get(field.type) for field in schema.fields}
    df = df.astype(dtypes_dict)

    return df


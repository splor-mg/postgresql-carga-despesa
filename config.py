import numpy as np
import os

FRICT_TO_DTYPES = {
    'string': object
    ,
    'number': np.float64
    ,
    'integer': np.int64
    ,
    'boolean': bool
    ,
    'null': None
    ,
    'object': object
    ,
    'datetime': np.datetime64[ns]
    ,
    'date': np.datetime64
    ,
    'time': np.datetime64
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


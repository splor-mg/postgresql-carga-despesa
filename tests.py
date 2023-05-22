from frictionless import Package

package = Package('datasets/despesa/data/datapackage.json')
#package.dereference()
print('name:', package.name)
print('sources:', package.sources)
print('resource_names:', package.resource_names)
print([r.name for r in package.resources])


print('GET_RESOURCE:', package.get_resource('dm_unidade_orc'))
print('PATH:', package.get_resource('dm_unidade_orc').path)
print('NAME:', package.get_resource('dm_unidade_orc').name)
print('BASEPATH:', package.get_resource('dm_unidade_orc').basepath)
print('REMOTE:', package.get_resource('dm_unidade_orc').remote)
print('FORMAT:', package.get_resource('dm_unidade_orc').format)


"""
__init__.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""

from tardis.tardis_portal.models.parameters import Schema
from tardis.tardis_portal.models.parameters import DatafileParameterSet


class ProteinStructureFilter(object):

    namespace = "http://tardis.edu.au/schemas/apps/jolecule/structure_file"
    name = "Jolecule Protein Structure 3D Viewer"

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):

        def isStructureFile(fileInstance):
            mimetype = fileInstance.get_mimetype()
            structureFileTypes = [
                "chemical/x-pdb",
            ]
            correct_mime = mimetype in structureFileTypes

            file_extension = fileInstance.filename.split(".")[-1]
            valid_extensions = [
                ".pdb",
            ]
            correct_extension = file_extension.lower() in valid_extensions
            return correct_mime or correct_extension

        instance = kwargs.get("instance")
        if isStructureFile(instance):
            if self.namespace not in \
               [set.schema.namespace for set in instance.getParameterSets()]:
                try:
                    theSchema = Schema.objects.get(
                        namespace__exact=self.namespace)
                except Schema.DoesNotExist:
                    theSchema = Schema(namespace=self.namespace,
                                       name=self.name,
                                       type=Schema.DATAFILE,
                                       hidden=True)
                    theSchema.save()
                myPS = DatafileParameterSet(schema=theSchema,
                                            dataset_file=instance)
                myPS.save()

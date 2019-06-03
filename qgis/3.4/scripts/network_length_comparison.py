from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class RoadNetworkLengthComparison(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('region', 'Region', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('regionid', 'Region ID', type=QgsProcessingParameterField.Any, parentLayerParameterName='region', allowMultiple=False, defaultValue='id'))
        self.addParameter(QgsProcessingParameterVectorLayer('roadnetwork1', 'Road Network 1', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('roadnetwork2', 'Road Network 2', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('OutputRoadNetworkComparison', 'Output Road Network Comparison', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Road Network Length
        alg_params = {
            'region': parameters['region'],
            'roadnetwork': parameters['roadnetwork2'],
            'qgis:sumlinelengths_1:Output Sum Road Network Length': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RoadNetworkLength'] = processing.run('model:Road Network Length', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Road Network Length
        alg_params = {
            'region': parameters['region'],
            'roadnetwork': parameters['roadnetwork1'],
            'qgis:sumlinelengths_1:Output Sum Road Network Length': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RoadNetworkLength'] = processing.run('model:Road Network Length', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['regionid'],
            'FIELDS_TO_COPY': None,
            'FIELD_2': parameters['regionid'],
            'INPUT': outputs['RoadNetworkLength']['qgis:sumlinelengths_1:Output Sum Road Network Length'],
            'INPUT_2': outputs['RoadNetworkLength']['qgis:sumlinelengths_1:Output Sum Road Network Length'],
            'METHOD': 1,
            'PREFIX': '',
            'NON_MATCHING': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lenDIFF',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': '\"length\" - \"length_2\"',
            'INPUT': outputs['JoinAttributesByFieldValue']['NON_MATCHING'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['OutputRoadNetworkComparison']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OutputRoadNetworkComparison'] = outputs['FieldCalculator']['OUTPUT']
        return results

    def name(self):
        return 'Road Network Length Comparison'

    def displayName(self):
        return 'Road Network Length Comparison'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return RoadNetworkLengthComparison()

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class RoadNetworkLength(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('region', 'Region', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('roadnetwork', 'Road Network', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('OutputSumRoadNetworkLength', 'Output Sum Road Network Length', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['roadnetwork'],
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['region'],
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Sum line lengths
        alg_params = {
            'COUNT_FIELD': 'COUNT',
            'LEN_FIELD': 'LENGTH',
            'LINES': outputs['ReprojectLayer']['OUTPUT'],
            'POLYGONS': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': parameters['OutputSumRoadNetworkLength']
        }
        outputs['SumLineLengths'] = processing.run('qgis:sumlinelengths', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OutputSumRoadNetworkLength'] = outputs['SumLineLengths']['OUTPUT']
        return results

    def name(self):
        return 'Road Network Length'

    def displayName(self):
        return 'Road Network Length'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return RoadNetworkLength()

from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Resultado import Resultado
from bson import ObjectId

class RepositorioResultado(InterfaceRepositorio[Resultado]):

    def getListadoVotosPorCandidato(self, id_candidato):
        theQuery = {"candidato.$id": ObjectId(id_candidato)}
        return self.query(theQuery)

    def getMayorNotaPorCandidato(self):
        query1={
                "$group": {
                    "_id": "$candidato",
                    "max": {
                        "$max": "$votos"
                    },
                    "doc": {
                        "$first": "$$ROOT"
                    }
                }
            }
        pipeline= [query1]
        return self.queryAggregation(pipeline)

    def promedioVotosPorCandidato(self,id_candidato):
        query1 = {
          "$match": {"candidato.$id": ObjectId(id_candidato)}
        }
        query2 = {
          "$group": {
            "_id": "$candidato",
            "promedio": {
              "$sum": "$votos"
            }
          }
        }
        pipeline = [query1, query2]
        return self.queryAggregation(pipeline)
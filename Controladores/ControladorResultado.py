from Modelos.Resultado import Resultado
from Modelos.Mesa import Mesa
from Modelos.Candidato import Candidato
from Repositorios.RepositorioResultado import RepositorioResultado
from Repositorios.RepositorioMesa import RepositorioMesa
from Repositorios.RepositorioCandidato import RepositorioCandidato

class ControladorResultado():
    def __init__(self):
        self.repositorioResultado = RepositorioResultado()
        self.repositorioMesas = RepositorioMesa()
        self.repositorioCandidatos = RepositorioCandidato()

    def index(self):
        return self.repositorioResultado.findAll()
    """
    Asignacion mesa y candidato a resultado
    """
    def create(self,infoResultado,id_mesa,id_candidato):
        nuevaResultado=Resultado(infoResultado)
        laMesa=Mesa(self.repositorioMesas.findById(id_mesa))
        elCandidato=Candidato(self.repositorioCandidatos.findById(id_candidato))
        nuevaResultado.mesa=laMesa
        nuevaResultado.candidato=elCandidato
        return self.repositorioResultado.save(nuevaResultado)

    def show(self,id):
        elResultado=Resultado(self.repositorioResultado.findById(id))
        return elResultado.__dict__
    """
    Modificación de resultado (mesa y candidato)
    """
    def update(self,id_resultado,infoVotos,id_mesa,id_candidato):
        elResultado=Resultado(self.repositorioResultado.findById(id_resultado))
        elResultado.votos = infoVotos["votos"]
        laMesa = Mesa(self.repositorioMesas.findById(id_mesa))
        elCandidato = Candidato(self.repositorioCandidatos.findById(id_candidato))
        elResultado.mesa = laMesa
        elResultado.candidato = elCandidato
        return self.repositorioResultado.save(elResultado)

    def delete(self, id):
        return self.repositorioResultado.delete(id)

    "Obtener todos los inscritos en una candidato"
    def listarVotosPorCandidato(self,id_candidato):
        return self.repositorioResultado.getListadoVotosPorCandidato(id_candidato)

    "Obtener candidatos mas votados"
    def votosMasAltosPorCandidato(self):
        return self.repositorioResultado.getMayorNotaPorCandidato()

    "Obtener promedio de votos por candidato"
    def promedioVotosPorCandidato(self,id_candidato):
        return self.repositorioResultado.promedioVotosPorCandidato(id_candidato)
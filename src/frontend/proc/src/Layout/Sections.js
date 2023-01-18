import Competitions from "../Procedures/Competitions";
import JogosMaisGolos from "../Procedures/JogosMaisGolos";
import EmpatesCompeticao from "../Procedures/EmpatesCompeticao";
import JogosCompeticao from "../Procedures/JogosCompeticao";
import JogosPor from "../Procedures/JogosPor";

const Sections = [

    {
        id: "competitions",
        label: "Competitions",
        content: <Competitions/>
    },

    {
        id: "jogos_golos",
        label: "Jogos com Mais Golos",
        content: <JogosMaisGolos/>
    },

    {
        id: "draws_competition",
        label: "Empates por Competição",
        content: <EmpatesCompeticao/>
    },
     {
        id: "games_competition",
        label: "Jogos por Competição",
        content: <JogosCompeticao/>
    },
     {
        id: "games_por",
        label: "Jogos Portugal por Data",
        content: <JogosPor/>
    }

];

export default Sections;
import Competitions from "../Tables/Competitions";
import Teams from "../Tables/Teams";
import Games from "../Tables/Games";

const Sections = [

    {
        id: "competitions",
        label: "Competitions",
        content: <Competitions/>
    },

    {
        id: "teams",
        label: "Teams",
        content: <Teams/>
    },

    {
        id: "games",
        label: "Games",
        content: <Games/>
    }

];

export default Sections;
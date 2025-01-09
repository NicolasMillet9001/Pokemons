var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var lang = urlParams.get('lang')

    const pokemonTypes = {
        "Normal": "Brown",
        "Feu": "Red",
        "Eau": "Blue",
        "Électrik": "Yellow",
        "Plante": "Green",
        "Glace": "LightBlue",
        "Combat": "Brown",
        "Poison": "Purple",
        "Sol": "Brown",
        "Vol": "SkyBlue",
        "Psy": "Pink",
        "Insecte": "LightGreen",
        "Roche": "Gray",
        "Spectre": "Purple",
        "Dragon": "Purple",
        "Ténèbres": "Black",
        "Acier": "Silver",
        "Fée": "Pink",
        
        "Normal": "Brown",
        "Fire": "Red",
        "Water": "Blue",
        "Electric": "Yellow",
        "Grass": "Green",
        "Ice": "LightBlue",
        "Fighting": "Brown",
        "Poison": "Purple",
        "Ground": "Brown",
        "Flying": "SkyBlue",
        "Psychic": "Pink",
        "Bug": "LightGreen",
        "Rock": "Gray",
        "Ghost": "Purple",
        "Dragon": "Purple",
        "Dark": "Black",
        "Steel": "Silver",
        "Fairy": "Pink"
    };

function getPokemonColor(type) {
    return pokemonTypes[type] || "Unknown";
}

var types = document.querySelectorAll(".type");

types.forEach(type => {
    var color = getPokemonColor(type.textContent);
    type.style.color = color;
})

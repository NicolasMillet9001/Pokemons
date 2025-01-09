var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var lang = urlParams.get('lang')
    
    var pokemons = document.querySelectorAll('.pokemon');
    
    const pokemonTypes = {
        "fr": [
            "Normal",
            "Feu",
            "Eau",
            "Électrik",
            "Plante",
            "Glace",
            "Combat",
            "Poison",
            "Sol",
            "Vol",
            "Psy",
            "Insecte",
            "Roche",
            "Spectre",
            "Dragon",
            "Ténèbres",
            "Acier",
            "Fée"
        ],
        
        "en": [
            "Normal",
            "Fire",
            "Water",
            "Electric",
            "Grass",
            "Ice",
            "Fighting",
            "Poison",
            "Ground",
            "Flying",
            "Psychic",
            "Bug",
            "Rock",
            "Ghost",
            "Dragon",
            "Dark",
            "Steel",
            "Fairy",
        ]
    };

    //Génère les options du choix du type avec les éléments de pokemonTypes en fonction de la langue
    var selectInput = document.querySelector("#select-pokemon-type");
    if(typeof(lang) != "undefined" && lang=="en"){
        pokemonTypes["en"].forEach((type) => {
            let option = document.createElement("option");
            option.value=type;
            option.textContent=type;
            selectInput.append(option);
        })
    }else{
        pokemonTypes["fr"].forEach((type) => {
            let option = document.createElement("option");
            option.value=type;
            option.textContent=type;
            selectInput.append(option);
        })
    }

    //js pour la search bar
    function UpdateDisplayedPokemons(){
        var inputName = document.querySelector('#searchbar').value.toLowerCase();
        var inputType = document.querySelector('#select-pokemon-type').value.toLowerCase();

        if (inputName == "" && inputType == ""){
            pokemons.forEach((pokemon) => {
                pokemon.style.display = "flex";
            })
        }else{
            pokemons.forEach((pokemon) => {
                if (pokemon.querySelector('.pokemon-name').textContent.toLowerCase().includes(inputName) && pokemon.querySelector('.pokemon-types').textContent.toLowerCase().includes(inputType)){
                    pokemon.style.display = "flex";
                }else{
                    pokemon.style.display = "none";
                }
            })
        }
    }

    //Fait apparaitre l'image d'un pokemon seulement lorsqu'il est affiché sur l'écran
    document.addEventListener("DOMContentLoaded", function() {
        const images = document.querySelectorAll('.lazy-load');
        const config = {
            rootMargin: '0px 0px 50px 0px',
            threshold: 0
        };
        const observer = new IntersectionObserver(function(entries, self) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    preloadImage(entry.target);
                    self.unobserve(entry.target);
                }
            });
        }, config);
        images.forEach(image => {
            observer.observe(image);
        });
        function preloadImage(img) {
            const src = img.getAttribute('data-src');
            if (!src) {
                return;
            }
            img.src = src;
            img.classList.add('loaded');
        }
    });


    //Rempli le champ caché pokemon-types pour le filtre type
    pokemons.forEach(pokemon => {
        var types = SetTypes(pokemon)
    });

    async function SetTypes(pokemon){
        const url = "/api/pokemons/"+pokemon.dataset.id;
        var result;

        try {
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            result = await response.json();
            // console.log(result);

            if (typeof(result["types"]["1"]) != "undefined"){
                pokemon.querySelector(".pokemon-types").textContent = result["types"]["0"]["name"][lang] + " " + result["types"]["1"]["name"][lang];
                SetBackgroundColor(pokemon, result["types"]["0"]["name"][lang],result["types"]["1"]["name"][lang]);
            }else{
                pokemon.querySelector(".pokemon-types").textContent = result["types"]["0"]["name"][lang]
                SetBackgroundColor(pokemon, result["types"]["0"]["name"][lang]);
            }

            
            
        } catch (error) {
            console.error(error.message);
        }
        return result;
    }

    const pokemonTypeColor = {
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
        return pokemonTypeColor[type] || "Unknown";
    }

    function SetBackgroundColor(divPokemon, type1, type2 = null){
        var color1 = getPokemonColor(type1);
        var color2;
        if (type2 != null){
            color2 = getPokemonColor(type2);
        }else{
            color2 = color1
        }
        divPokemon.style = "background-image: linear-gradient(to left top, "+ color1 +",white,"+ color2 +")";
    }

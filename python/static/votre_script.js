// Exemple de données (à remplacer par vos propres données)
var data = [{
    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    y: [20, 35, 25, 30, 15],
    type: 'bar',
    marker: {
        color: 'blue'
    }
}];

// Mise en page du graphique
var layout = {
    title: 'Exemple de graphique à barres',
    xaxis: {
        title: 'Mois'
    },
    yaxis: {
        title: 'Valeur'
    }
};

// Afficher le graphique dans le conteneur spécifié
Plotly.newPlot('plotly-chart', data, layout);

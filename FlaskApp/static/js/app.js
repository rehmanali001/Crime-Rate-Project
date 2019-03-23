function buildCharts(state) {
    // TO DO: Iterate through all states

    d3.json(`/metadata/state/${state}`, function(stateData) {
        console.log(state);

        // Cast rates as numbers
        console.log('state data', stateData);
        
        // Build line chart
	    var trace1 = {
            x: stateData.year,
            y: stateData.crime_rates,
            type: "line",
            text: 'Counts per 1,000'
            
        };
        var data = [trace1];
        var layout = {
            title: `${state} Crime Rates`,
            xaxis: { title: "Year"},
            yaxis: { title: "Crime Rate"}
        };
        Plotly.newPlot("line", data, layout);        
    });

    // Build map with 2014 data
    d3.json(`/metadata/year/2014`, function(yearData) {
        console.log('2014 data', yearData)


        // Build bar chart
        var myPlot = document.getElementById('bar'),
            data = [{
                x: yearData.states,
                y: yearData.crime_rates,
                type: "bar",
                marker: {
                    color: 'light blue'
                },
                text: 'Counts per 1,000',
            }];
            layout = {
                title: "2014 Crime Rates",
                xaxis: { 
                    tickangle: 40,
                    tickfont: {
                        size: 9.5
                    }
                },
                yaxis: {title: "Crime Rate"},
                hovermode: 'closest'
            };

        Plotly.newPlot("bar", data, layout);

    });
    
}

function init() {      

    // Set up the dropdown menu
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/states").then((state) => {
        state.forEach((instance) => {
        selector
            .append("option")
            .text(instance)
            .property("value", instance);
        });

        // Use Alabama to build the initial plot
        const defaultState = state[0];
        buildCharts(defaultState);
    });
}

function optionChanged(newState) {
    // Fetch new data each time a new state is selected
    buildCharts(newState);
}

init();
alert('If you see this alert, then your custom JavaScript script has run!')


function init_cy(){
    let cy = window.cy;
    window.complete_elements = cy.elements();
    window.complete_elements_copy = window.complete_elements.clone();

    window.cy.on('mouseover', 'node', function(e) {
        let sel = e.target;
        cy.elements()
            .difference(sel.outgoers()
                .union(sel.incomers()))
            .not(sel)
            .addClass('semitransp');
        sel.addClass('highlight')
            .outgoers()
            .union(sel.incomers())
            .addClass('highlight');
    });

    window.cy.on('mouseout', 'node', function(e) {
        let sel = e.target;
        cy.elements()
            .removeClass('semitransp');
        sel.removeClass('highlight')
            .outgoers()
            .union(sel.incomers())
            .removeClass('highlight');
    });

    // 🚩 Add Click Event on Node (this is a walk-around solution) >>>
    window.cy.on('click', 'node', function(e) {
        var val = alert(`Node id: ${e.target.id()}`);

    }); // # 🚩<<<
}



function init_slider(){
    document.getElementById('node-slider').addEventListener("change", function(e){
      let cy = window.cy;
    //   // Remove all elements first
      cy.elements().remove()
    //   // Add all elements then; This is more convenient to compute nodes to remove in the original graph than subgraph. 
      cy.add(window.complete_elements_copy);
      var complete_nodes = cy.nodes();
      let percentage = Number(e.target.value);
      let total_length = complete_nodes.length;
      let threshold = total_length * percentage;
      let node2remove = complete_nodes.filter(`node[rank > ${threshold}]`)
      cy.remove(node2remove);

    });
}

function init_callbacks(){
    init_cy();
    init_slider();
}

// When the page is load we add our customized JS code on it to extend functions
// window.addEventListener('load', (event) => {
    
// });

init_callbacks()
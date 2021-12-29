const form = document.querySelector("#cupcake-form")

form.addEventListener("submit", async function(event) {
    event.preventDefault()
    const cupcake = new Cupcake(
            document.querySelector("#flavor").value,
            document.querySelector("#size").value,
            document.querySelector("#rating").value,
            document.querySelector("#image").value
        );
    cupcakes.addCupcake(cupcake);
})

const ul = document.querySelector("#cupcake-list")
ul.addEventListener("click", async function(event) {
    if (event.target.classList.value == 'deleteCup') {
        const cupcakeId = event.target.parentElement.dataset.id
        const resp = await axios.delete("http://127.0.0.1:5000/api/cupcakes/"+cupcakeId)
        if(resp.data.message = "Deleted") {
            event.target.parentElement.remove()
        }
        
    }
    
})

class Cupcake {
    constructor(flavor, size, rating, image) {
        this.flavor = flavor;
        this.size = size;
        this.rating = rating;
        this.image = image;
    }
}

class Cupcakes {
    constructor(){
        this.createCupcakeList()
    }

    async createCupcakeList() {
        const ul = document.querySelector("#cupcake-list")
        const cupcakes = await this.getAllCupcakes()
        this.removeAllElements(ul);
        for (const cupcake of cupcakes) {
            ul.append(this.createCupList(cupcake));
        }
    }

    createCupList(cupcake) {
        const li = document.createElement("li");
        li.innerText = `${cupcake.flavor} ${cupcake.size}`;
        li.dataset.id = cupcake.id;
        const deleteButton = document.createElement("button")
        deleteButton.innerText = "X";
        deleteButton.classList.add("deleteCup");
        li.append(deleteButton);
        return li;
    }

    
    async getAllCupcakes() {
        let response = await axios.get("http://127.0.0.1:5000/api/cupcakes")
        return response.data.cupcakes;
    }

    removeAllElements(parent) {
        while(parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }

    async addCupcake(cupcake) {
        let response = await axios.post("http://127.0.0.1:5000/api/cupcakes", cupcake)
        cupcake = response.data.cupcake;
        const ul = document.querySelector("#cupcake-list");
        ul.append(this.createCupList(cupcake));
    }

}

const cupcakes = new Cupcakes();


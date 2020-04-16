Vue.component('search', {
    data: function() {
        return {
            q: '',
            results: [],
        }
    },
    template: `
    <div>
        <div class="w3-row">
            <div class="w3-col w3-panel l5 m12 s12">
                <div class="w3-row w3-padding w3-card w3-round-large">
                    <form v-on:submit="search($event)">
                        <div class="w3-col l11 m11 s11">
                            <input v-model="q" 
                                type="text" 
                                class="w3-input" 
                                placeholder=" Search" 
                                style="font-family: Arial, FontAwesome" />
                        </div>
                        <div class="w3-col l1 m1 s1">
                            <button type="submit" 
                                v-on:submit="search($event)" 
                                class="w3-right" 
                                style="background: none; border: none; margin-top: 8px" >
                                
                                <i class="fa fa-search"></i>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <results :results="results" class="max-height"></results>
    </div>

    `,
    methods: {
        search: function(event) {
            event.preventDefault();
            var vm = this;
            if (!vm.q) {
                return;
            }
            fetch('search?q=' + vm.q)
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    vm.results = json;
                });
        }
    }
})
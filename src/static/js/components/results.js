Vue.component('results', {
    props: [ 'results' ],
    data: function() {
        return {
            selected: null,
            hovering: {
                flag: false,
                res: null
            }
        }
    },
    template: `
    <div class="w3-row">
        <div class="w3-col w3-panel l5 m12 s12">
            <ul class="w3-ul w3-hoverable" style="height: 100%; padding-top: 16px;">
                <li class="cursor-hover" 
                    v-for="res in results"
                    v-on:mouseover="setHovering(res)" 
                    v-on:mouseleave="unsetHovering()"
                    style="height: 125px; cursor: pointer" v-on:click="select(res)">

                    <p class="two-line-limit">{{ res.matches.join('...') }}</p>
                    <p class="w3-right">{{ res.file }}(p{{ res.page }})</p>
                </li>
            </ul>
        </div>
        <div class="w3-col w3-panel l7 m12 s12">
            <display v-bind:selected="selected" v-bind:hovering="hovering"></display>
        </div>
    </div>
    `,
    methods: {
        select: function(result) {
            var vm = this;
            vm.selected = result;
        },
        setHovering: function(result) {
            var vm = this;
            vm.hovering.flag = true;
            vm.hovering.res = result;
        },
        unsetHovering: function(result) {
            var vm = this;
            vm.hovering.flag = false;
            vm.hovering.res = null;
        }
    }
})
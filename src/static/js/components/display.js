Vue.component('display', {
    props: [ 'selected', 'hovering' ],
    template: 
    `<div class="max-height" v-if="selected || hovering.flag">
        <div class="w3-bar">
            <button v-on:click="left(selected)" class="w3-button w3-left" style="width: 40%">
                <i class="fa fa-arrow-left"><i>
            </button>
            <button class="w3-button w3-left" style="width: 20%">{{ selected.page }}</button>
            <button v-on:click="right(selected)" class="w3-button w3-right" style="width: 40%">
                <i class="fa fa-arrow-right"><i>
            </button>
        </div>
        <img 
            :src="getFilename(hovering, selected)" 
            width="100%" 
            height="100%">
        </img>
    </div>`,
    methods: {
        getFilename: function(hovered, selected) {
            let filename, page;
            if (hovered.flag) {
                filename = hovered.res.file;
                page = hovered.res.page;
            } else {
                filename = selected.file;
                page = selected.page;
            }

            const filenameNoExt = filename.replace('.pdf', '');
            return "static/img/" + filenameNoExt + '/' + page + '.jpg';
        },

        left: function(selected) {
            var vm = this;
            vm.selected = {
                file: selected.file,
                page: selected.page - 1,
                text: ''
            }
        },

        right: function(selected) {
            var vm = this;
            vm.selected = {
                file: selected.file,
                page: selected.page + 1,
                text: ''
            }
        }
    }
})
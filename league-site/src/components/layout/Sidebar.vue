<template>
    <sidebar-menu 
    :menu="menu" 
    :collapsed="true"
    >
    <span slot="collapse-icon" class="fas fa-arrows-alt-h"></span>
    </sidebar-menu >
</template>

<script>
import { SidebarMenu } from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import '@fortawesome/fontawesome-free/css/all.css'
export default {
  name:"Sidebar",
  components: {
    SidebarMenu
  },
        data() {
        return {
            menu: [
                {
                    header: true,
                    title: 'Main Navigation'
                },
                {
                    title:'Announcements',
                    href: '/announcements',
                    icon: 'fa fa-download'
                }
            ]
        }
    }
}
</script>

<style>
.v-sidebar-menu .vsm-arrow:after{font-family: FontAwesome}
.v-sidebar-menu .collapse-btn:after {
content: "\f07e";
font-family: FontAwesome;
}
</style>

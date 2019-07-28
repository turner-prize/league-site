<template>
    <sidebar-menu 
    :menu="menu" 
    :collapsed="true"
    >
    <span slot="collapse-icon" class="fas fa-arrows-alt-h"></span>
    <span slot="dropdown-icon" class="fas fa-angle-down"></span>
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
                    href: '/announcementsView',
                    icon: 'far fa-comment-alt'
                },
                {
                    title:'Table',
                    href: '/tableView',
                    icon: 'fas fa-table'
                },
                { // item with child
                        title: 'Charts',
                        icon: 'fa fa-chart-area',
                        child: [
                            {
                                href: '/statsView',
                                title: 'League Table over Time',
                            }
                        ]
                    },
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

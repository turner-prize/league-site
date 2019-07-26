<template>
    <sidebar-menu 
    :menu="menu" 
    :collapsed="true"
    />
</template>

<script>
import { SidebarMenu } from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
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
                    title:'test',
                    href: '/about',
                    icon: 'fa fa-download'
                }
            ]
        }
    }
}
</script>

<style>

</style>

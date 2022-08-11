<template id="navigation-drawer">
<v-container>
	<v-app-bar app>
		<v-app-bar-nav-icon @click.stop='drawerIsOpen = !drawerIsOpen'/>
		<v-app-bar-title>
			Sign language API
		</v-app-bar-title>
	</v-app-bar>
	<v-navigation-drawer v-model='drawerIsOpen' temporary app>
		<v-list-item>
			<v-list-item-content>
				<v-list-item-title class='text-h6'>
					Site navigation
				</v-list-item-title>
				<v-list-item-subtitle>
					Click a link below
				</v-list-item-subtitle>
			</v-list-item-content>
		</v-list-item>
		<v-divider />
		<v-list-item
			v-for='link in links'
			:key='link.pageName'
			link
			:to='link.path'
		>
			<v-list-item-icon>
				<v-icon>{{link.icon}}</v-icon>
			</v-list-item-icon>
			<v-list-item-content>
				<v-list-item-title>{{link.pageName}}</v-list-item-title>
			</v-list-item-content>
		</v-list-item>
	</v-navigation-drawer>
</v-container>
</template>

<script charset="utf-8">
export default {
  data: () => ({
		links: [
			{ icon: 'mdi-home', pageName: 'Browse libraries', path:'/'},
			{ icon: 'mdi-cloud-upload', pageName: 'Upload a library', path:'/library/upload'},
			{ icon: 'mdi-video-check', pageName: 'Test a library', path: '/library/test'}
		],
		drawerIsOpen: false
  }),
}
</script>

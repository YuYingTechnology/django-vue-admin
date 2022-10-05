<template>
    <div>
        <span>用户组（角色）权限</span>
        <el-tabs tab-position="left" style="height: 200px;">
            <el-tab-pane label="用户管理">用户管理</el-tab-pane>
            <el-tab-pane label="配置管理">配置管理</el-tab-pane>
            <el-tab-pane label="角色管理">角色管理</el-tab-pane>
            <el-tab-pane label="定时任务补偿">定时任务补偿</el-tab-pane>
        </el-tabs>
        <span>用户权限</span>
        <el-tabs tab-position="left" style="height: 200px;">
            <el-tab-pane label="用户管理">用户管理</el-tab-pane>
            <el-tab-pane label="配置管理">配置管理</el-tab-pane>
            <el-tab-pane label="角色管理">角色管理</el-tab-pane>
            <el-tab-pane label="定时任务补偿">定时任务补偿</el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: 'Permissions',
    // components: {
    //     CustomTable
    // },
    computed: {
        ...mapGetters([
            'height',
            'width'
        ])
    },

    data() {
        return {
            queryParams: {
                size: 500,
                page: 1,
                search: '',
                ordering: '',
            },
            tabPosition: 'left',
        }
    }
}
</script>

<style>

</style>
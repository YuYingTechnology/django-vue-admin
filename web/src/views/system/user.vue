<template>
    <div>
        <div style="margin: 10px 0 0 0">
            <el-tabs
                v-model="activeName"
                @tab-click="fetchDataAction"
                type="border-card"
                stretch>
                <el-tab-pane label="本地用户" name="local"></el-tab-pane>
                <el-tab-pane label="企业微信用户" name="wechat"></el-tab-pane>
                <el-tab-pane label="飞书用户" name="feishu"></el-tab-pane>
                <el-tab-pane label="钉钉用户" name="dintalk"></el-tab-pane>
            </el-tabs>
            <el-input
                v-model="queryParams.search"
                style="width: 250px; margin: 10px 0 0 10px"
                clearable
                :placeholder="activeName == 'local' ? '输入id、用户名、姓名、邮箱搜索' : activeName == 'wechat' ? '输入id、企业微信id搜索' : activeName == 'feishu' ? '输入关键字搜索' : '输入关键字搜索'">
            </el-input>
            <!-- <el-button type="primary" @click="fetchDataAction()">搜索</el-button> -->
            <el-pagination
                style="text-align: right;margin: -30px 10px 0 0"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :page-sizes="[1, 20, 50, 100, 200, 400, 500]"
                :page-size="20"
                layout="total, sizes, prev, pager, next, jumper"
                :total="activeName == 'local' ? total : activeName == 'wechat' ? wechatTotal : activeName == 'feishu' ? feiShuTotal : dingtalkTotal">
            </el-pagination>
        </div>
        <el-table
            v-loading="isLoading"
            @sort-change="handleSortChange"
            border
            :data="activeName == 'local' ? data : activeName == 'wechat' ? wechatData : activeName == 'feishu' ? feiShuData : dingtalkData"
            style="width: 100%;margin: 10px 0 0 0"
            :height="height + 'px'">
            <el-table-column
                type="index"
                label="序号"
                width="50">
            </el-table-column>
            <el-table-column
                v-for="(item, index) in (activeName == 'local' ? tableColumnData : activeName == 'wechat' ? wechatTableColumnData : activeName == 'feishu' ? feiShuTableColumnData : dingtalkTableColumnData)"
                :key="index"
                :prop="item.prop"
                :label="item.label"
                sortable>
                <template slot-scope="scope"> 
                    <el-switch 
                        v-if="item.is_boolean_field"
                        @change="updateLocalUser(scope.row.id, { [item.prop]: scope.row[item.prop] })"
                        v-model="scope.row[item.prop]"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                    </el-switch>
                    <el-avatar v-else-if="item.prop == 'avatarUrl' || item.prop == 'avatar_big'" size="large" :src="scope.row[item.prop]"></el-avatar>
                    <span v-else-if="item.prop == 'wechat' && scope.row[item.prop] != null">{{ scope.row[item.prop].userid }}</span>
                    <span v-else-if="item.prop == 'groups' && scope.row[item.prop] != []" v-for="item in scope.row[item.prop]" :key='item.id'>
                        <el-tag size="medium">{{ item.name }}</el-tag>
                    </span>
                    <span v-else-if="item.prop == 'user_permissions'">
                        <el-button size="small" v-if="activeName == 'local'" @click="dialogPermissionsVisible = true; userPermissionsData = scope.row[item.prop]">查看</el-button>
                    </span>
                    <span v-else>{{ scope.row[item.prop] }}</span>
                </template>

            </el-table-column>
            <el-table-column
                fixed="right"
                label="操作"
                width="300">
                <template slot-scope="scope">
                    <el-button type="text" size="small" v-if="activeName == 'local'" @click="dialogFormVisible = true; handleUpdateLocalUser(scope.row); getWechatList(); getFeiShuList(); getDingtalkList(); getGroupsList()">编辑</el-button>
                    <el-divider direction="vertical"></el-divider>
                    <el-popover
                        placement="top"
                        width="200">
                        <p>确定删除该条数据吗？</p>
                        <div style="text-align: right; margin: 0">
                            <!-- <el-button size="mini" type="text" @click="visible = false">取消</el-button> -->
                            <el-button type="primary" size="mini" @click="deleteDataAction(scope.row.id)">确定</el-button>
                        </div>
                        <el-button type="text" style="color: #f56c6c;" size="small" slot="reference">删除</el-button>
                    </el-popover>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog 
            center :title="'用户： ' + dataForm.username" 
            :visible.sync="dialogFormVisible">
                <el-form :inline="true" :model="dataForm">
                    <el-form-item label="用户名：" label-width="120px">
                        <el-input v-model="dataForm.username" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="姓氏：" label-width="120px">
                        <el-input v-model="dataForm.last_name" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="名字：" label-width="120px">
                        <el-input v-model="dataForm.first_name" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱：" label-width="120px">
                        <el-input v-model="dataForm.email" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="用户分组：" label-width="120px">
                        <el-select v-model="dataForm.groups" multiple placeholder="请选择用户分组"  @change="refreshData">
                            <el-option
                                v-for="item in groupsData" 
                                :key="item.id" 
                                :label="item.name" 
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="企业微信账号：" label-width="120px">
                        <el-select v-model="dataForm.wechat" clearable placeholder="请绑定企业微信">
                            <el-option
                                v-for="item in wechatData"
                                :key="item.id"
                                :label="item.userid"
                                :value="item.id"
                                :disabled="item.bound">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="飞书账号：" label-width="120px">
                        <el-select v-model="dataForm.feishu" placeholder="请绑定飞书">
                            <div v-for="item in feiShuData" :key="item.id">
                                <el-option :label="item.userid" :value="item.userid"></el-option>
                            </div>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="钉钉账号：" label-width="120px">
                        <el-select v-model="dataForm.dingtalk" placeholder="请绑定钉钉">
                            <div v-for="item in dingtalkData" :key="item.id">
                                <el-option :label="item.nick" :value="item.id"></el-option>
                            </div>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="dialogFormVisible = false; updateLocalUser(dataForm.id, dataForm)">确 定</el-button>
                </div>
        </el-dialog>
        <el-dialog
            title="提示"
            :visible.sync="dialogPermissionsVisible"
            center>
            <span>
                {{ userPermissionsData }}
            </span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPermissionsVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogPermissionsVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
  
<script>
// import CustomTable from '@/components/Table'
import { mapGetters } from 'vuex'
import { 
    getUserList, createUser, updateUser, deleteUser,
    getWechatList, updateWechat, deleteWechat,
    getFeiShuList, updateFeiShu, deleteFeiShu,
    getDingtalkList, updateDingtalk, deleteDingtalk,
    getGroupsList
} from '@/api/user'

export default {
    name: 'User',
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
                size: 20,
                page: 1,
                search: '',
                ordering: '',
            },
            total: 0,
            wechatTotal: 0,
            feiShuTotal: 0,
            dingtalkTotal: 0,
            data: [],
            tableColumnData: [],
            wechatTableColumnData: [],
            feiShuTableColumnData: [],
            dingtalkTableColumnData: [],
            isLoading: false,
            activeName: 'local',
            dataForm: {},
            dialogFormVisible: false,
            dialogPermissionsVisible: false,
            wechatData: [],
            feiShuData: [],
            dingtalkData: [],
            groupsData: [],
            userPermissionsData: [],
        }
    },
    watch: {
        // 实时监听搜索框
        'queryParams.search':{
            handler(val){
                this.fetchDataAction()
            }
        }
    },
    mounted() {
        this.fetchDataAction()
        var el_tabs_content = document.querySelector('.el-tabs__content')
        el_tabs_content.remove()
    },
    methods: {
        refreshData () {
            this.$forceUpdate()
        },
        handleSortChange(sortData){
            console.log(sortData);
            if(sortData.order == "descending"){
                this.queryParams.ordering = '-' + sortData.prop
            } else {
                this.queryParams.ordering = sortData.prop
            }
            // Django 后端的方法，只允许当前页排序，没多大意义，暂时注释
            // this.fetchDataAction()
        },
        fetchDataAction() {
            this.data = []
            this.total = 0
            this.tableColumnData = []
            switch(this.activeName) {
                case 'local':
                    this.getUserList();
                    break;
                case 'wechat':
                    this.getWechatList();
                    break;
                case 'feishu':
                    this.getFeiShuList();
                    break;
                case 'dintalk':
                    this.getDingtalkList();
                    break;
            }
        },
        deleteDataAction(id) {
            switch(this.activeName) {
                case 'local':
                    this.deleteLocalUser(id);
                    break;
                case 'wechat':
                    this.deleteWechatUser(id);
                    break;
                case 'feishu':
                    this.deleteFeiShuUser(id);
                    break;
                case 'dintalk':
                    this.deleteDingtalkUser(id);
                    break;
            }

        },
        getUserList() {
            this.isLoading = true
            getUserList(this.queryParams).then(response => {
                this.isLoading = false
                console.log('getUserList===============', response)
                this.data = response.data.results
                this.total = response.data.count
                this.tableColumnData = response.data.column_list
            }).catch(error => {
                this.isLoading = false
                console.log('getUserList===============', error)
            })
        },
        getWechatList() {
            this.isLoading = true
            getWechatList(this.queryParams).then(response => {
                this.isLoading = false
                console.log('getWechatList===============', response)
                this.wechatData = response.data.results
                this.wechatTotal = response.data.count
                this.wechatTableColumnData = response.data.column_list
                return response
            }).catch(error => {
                this.isLoading = false
                console.log('getWechatList===============', error)
            })
        },
        getFeiShuList() {
            this.isLoading = true
            getFeiShuList(this.queryParams).then(response => {
                this.isLoading = false
                console.log('getFeiShuList===============', response)
                this.feiShuData = response.data.results
                this.feiShuTotal = response.data.count
                this.feiShuTableColumnData = response.data.column_list
            }).catch(error => {
                this.isLoading = false
                console.log('getFeiShuList===============', error)
            })
        },
        getDingtalkList() {
            this.isLoading = true
            getDingtalkList(this.queryParams).then(response => {
                this.isLoading = false
                console.log('getDingtalkList===============', response)
                this.dingtalkData = response.data.results
                this.dingtalkTotal = response.data.count
                this.dingtalkTableColumnData = response.data.column_list
            }).catch(error => {
                this.isLoading = false
                console.log('getDingtalkList===============', error)
            })
        },
        getGroupsList () {
            getGroupsList().then(response => {
                console.log('getGroupsList===============', response)
                this.groupsData = response.data.results
            })
        },
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`);
            this.queryParams.page = 1
            this.queryParams.size = val
            this.fetchDataAction()
        },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
            this.queryParams.page = val
            this.fetchDataAction()
        },
        deleteLocalUser(id) {
            deleteUser(id).then(response => {
                console.log('deleteLocalUser=======', response)
                this.fetchDataAction()
                this.$message({
                    showClose: true,
                    message: '删除成功',
                    type: 'success'
                });
            }).catch(error => {
                this.isLoading = false
                console.log('deleteLocalUser===============', error)
                this.$message({
                    showClose: true,
                    message: '删除失败',
                    type: 'error'
                });
            })
        },
        deleteWechatUser(id) {
            deleteWechat(id).then(response => {
                console.log('deleteWechat=======', response)
                this.fetchDataAction()
                this.$message({
                    showClose: true,
                    message: '删除成功',
                    type: 'success'
                });
            }).catch(error => {
                this.isLoading = false
                console.log('deleteWechatUser===============', error)
                this.$message({
                    showClose: true,
                    message: '删除失败',
                    type: 'error'
                });
            })
        },
        deleteFeiShuUser(id) {
            deleteFeiShu(id).then(response => {
                console.log('deleteFeiShuUser=======', response)
                this.fetchDataAction()
                this.$message({
                    showClose: true,
                    message: '删除成功',
                    type: 'success'
                });
            }).catch(error => {
                this.isLoading = false
                console.log('deleteFeiShuUser===============', error)
                this.$message({
                    showClose: true,
                    message: '删除失败',
                    type: 'error'
                });
            })
        },
        deleteDingtalkUser(id) {
            deleteDingtalk(id).then(response => {
                console.log('deleteDingtalkUser=======', response)
                this.fetchDataAction()
                this.$message({
                    showClose: true,
                    message: '删除成功',
                    type: 'success'
                });
            }).catch(error => {
                this.isLoading = false
                console.log('deleteDingtalkUser===============', error)
                this.$message({
                    showClose: true,
                    message: '删除失败',
                    type: 'error'
                });
            })
        },
        handleUpdateLocalUser(dataForm) {
            this.dataForm = structuredClone(dataForm);
            if (dataForm.wechat != null && 'id' in dataForm.wechat) {
                this.dataForm.wechat = dataForm.wechat.id
            }
            if (dataForm.feishu != null && 'id' in dataForm.feishu) {
                this.dataForm.feishu = dataForm.feishu.id
            }
            if (dataForm.dintalk != null && 'id' in dataForm.dintalk) {
                this.dataForm.dintalk = dataForm.dintalk.id
            }
            this.dataForm.groups = []
            dataForm.groups.forEach(element => {
                this.dataForm.groups.push(element.id)
            });
            console.log(this.dataForm)
        },
        updateLocalUser(id, data) {
            this.isLoading = true
            updateUser(id, data).then(response => {
                this.loading = false
                console.log('updateLocalUser=======', response)
                this.fetchDataAction()
                this.$message({
                    showClose: true,
                    message: '更新成功',
                    type: 'success'
                });
                this.fetchDataAction()
            }).catch(error => {
                this.isLoading = false
                console.log('updateLocalUser===============', error)
                this.loading = false
                this.$message({
                    showClose: true,
                    message: '更新失败',
                    type: 'error'
                });
                this.fetchDataAction()
            })
        }
    },
}
</script>

<style>
::v-deep .el-tabs__nav-scroll{
	width:50%;
	margin:0 auto
}
</style>
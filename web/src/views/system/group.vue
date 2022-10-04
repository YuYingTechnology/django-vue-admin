<template>
    <div>
        <el-input
            v-model="queryParams.search"
            style="width: 250px; margin: 10px 0 0 10px"
            clearable
            placeholder="输入用户组名称搜索">
        </el-input>
        <el-button
            type="primary"
            style="margin: 0 0 0 10px"
            @click="dialogFormVisible = true;">
            新建
        </el-button>
        <el-pagination
            style="text-align: right; margin: -30px 10px 0 0"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :page-sizes="[1, 20, 50, 100, 200, 400, 500]"
            :page-size="20"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
        </el-pagination>
        <el-table
            ref="tableRef"
            v-loading="isLoading"
            border
            :data="data"
            style="width: 100%; margin: 10px 0 0 0"
            :height="height + 'px'">
            <el-table-column
                type="index"
                label="序号"
                width="50">
            </el-table-column>
            <el-table-column
                v-for="(item, index) in tableColumnData"
                :key="index"
                :prop="item.prop"
                :label="item.label"
                sortable>
            </el-table-column>
            <el-table-column
                fixed="right"
                label="操作"
                min-width="120px"
                width="400">
                <!-- <template slot="header" slot-scope="scope">
                    <el-button type="text" size="small" @click="dialogFormVisible = true;">新建</el-button>
                    <el-divider direction="vertical"></el-divider>
                    <el-input
                        v-model="queryParams.search"
                        size="mini"
                        style="width: 150px"
                        @input.native="getUserGroupList()"
                        placeholder="输入用户组名称搜索">
                    </el-input>
                </template> -->
                <template slot-scope="scope">
                    <el-button type="text" size="small" @click="dialogFormVisible = true; handleUpdateGroup(scope.row)">编辑</el-button>
                    <el-divider direction="vertical"></el-divider>
                    <el-popover
                        placement="top"
                        width="200">
                        <p>确定删除该条数据吗？</p>
                        <div style="text-align: right; margin: 0">
                            <!-- <el-button size="mini" type="text" @click="visible = false">取消</el-button> -->
                            <el-button type="primary" size="mini" @click="deleteUserGroup(scope.row.id)">确定</el-button>
                        </div>
                        <el-button type="text" style="color: #f56c6c;" size="small" slot="reference">删除</el-button>
                    </el-popover>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog :title="dataForm.id ? '用户组： ' + dataForm.name : '新建用户组'" :visible.sync="dialogFormVisible" @closed="dataForm={}" width="400px">
            <el-form :inline="true" :model="dataForm">
                <el-form-item label="用户组名称：" label-width="120px">
                    <el-input v-model="dataForm.name" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button v-if="dataForm.id" type="primary" @click="dialogFormVisible = false; updateUserGroup(dataForm.id, dataForm)">确 定</el-button>
                <el-button v-else type="primary" @click="dialogFormVisible = false; createUserGroup(dataForm)">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    // import CustomTable from '@/components/Table'
    import { mapGetters } from 'vuex'
    import { 
        getUserGroupList, createUserGroup, updateUserGroup, deleteUserGroup, 
    } from '@/api/group'
    
    export default {
        name: 'Groups',
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
                    page: 1
                },
                isLoading: true,
                dialogFormVisible: false,
                data: [],
                total: 0,
                tableColumnData: [],
                dataForm: {
                    'name': '',
                }
            }
        },
        watch: {
            data: {
                handler() {
                this.$nextTick(() => {
                    // tableRef是el-table绑定的ref属性值
                    this.$refs.tableRef.doLayout()
                })
                },
                deep: true,
            },
            // 实时监听搜索框
            'queryParams.search':{
                handler(val){
                    this.getUserGroupList()
                }
            }
        },
        mounted() {
            this.getUserGroupList()
        },
        methods: {
            getUserGroupList() {
                this.isLoading = true
                getUserGroupList(this.queryParams).then(response => {
                    this.isLoading = false
                    console.log('getUserGroupList===============', response)
                    this.data = response.data.results
                    this.total = response.data.count
                    this.tableColumnData = response.data.column_list
                }).catch(error => {
                    this.isLoading = false
                    console.log('getUserGroupList===============', error)
                    this.loading = false
                })
            },
            createUserGroup(data) {
                this.isLoading = true
                createUserGroup(data).then(response => {
                    this.isLoading = false
                    console.log('createUserGroup===============', response)
                    this.getUserGroupList()
                    this.$message({
                        showClose: true,
                        message: '新建成功',
                        type: 'success'
                    });
                }).catch(error => {
                    this.isLoading = false
                    console.log('getUserGroupList===============', error)
                })
            },
            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
                this.queryParams.page = 1
                this.queryParams.size = val
                this.getUserGroupList()
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
                this.queryParams.page = val
                this.getUserGroupList()
            },
            updateUserGroup(groupId, data) {
                updateUserGroup(groupId, data).then(response => {
                    this.isLoading = false
                    console.log('updateUserGroup===============', response)
                    this.getUserGroupList()
                    this.$message({
                        showClose: true,
                        message: '更新成功',
                        type: 'success'
                    });
                }).catch(error => {
                    this.isLoading = false
                    console.log('updateUserGroup===============', error)
                    this.$message({
                        showClose: true,
                        message: '更新失败',
                        type: 'error'
                    });
                })
            },
            deleteUserGroup(groupId) {
                deleteUserGroup(groupId).then(response => {
                    this.isLoading = false
                    console.log('deleteUserGroup===============', response)
                    this.getUserGroupList()
                    this.$message({
                        showClose: true,
                        message: '删除成功',
                        type: 'success'
                    });
                }).catch(error => {
                    this.isLoading = false
                    console.log('deleteUserGroup===============', error)
                    this.$message({
                        showClose: true,
                        message: '删除失败',
                        type: 'error'
                    });
                })
            },
            
            handleUpdateGroup(dataForm) {
                this.dataForm = structuredClone(dataForm);
            }
        }
    }
</script>
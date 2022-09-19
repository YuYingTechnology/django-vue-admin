<template>
    <div>
        <el-pagination
            style="text-align: center"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :page-sizes="[1, 20, 50, 100, 200, 400, 500]"
            :page-size="20"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
        </el-pagination>
        <el-table
            border
            :data="data"
            style="width: 100%"
            height="250">
            <el-table-column
                v-for="(item, index) in tableColumnData"
                :key="index"
                :prop="item.prop"
                :label="item.label"
                sortable
            >
            </el-table-column>
            <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
                <el-button type="text" size="small">编辑</el-button>
                <el-button type="text" size="small">删除</el-button>
            </template>
            </el-table-column>
        </el-table>
    </div>
  </template>
  
<script>
// import CustomTable from '@/components/Table'
import { getUserList } from '@/api/user'

export default {
    name: 'user',
    // components: {
    //     CustomTable
    // },

    data() {
        return {
            queryParams: {
                size: 20,
                page: 1
            },
            total: 0,
            data: [],
            tableColumnData: [],
        }
    },
    mounted() {
        this.fetchDataAction()
    },
    methods: {
        fetchDataAction() {
            getUserList(this.queryParams).then(response => {
                console.log('getUserList===============', response)
                this.data = response.data.results
                this.total = response.data.count
                this.tableColumnData = response.data.results[0].column_list
            }).catch(error => {
                console.log('getUserList===============', error)
                this.loading = false
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
        }
    },
}
</script>

<style>

</style>
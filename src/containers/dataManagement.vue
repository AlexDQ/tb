<template>
    <div id='dataManagement' style='padding:20px'>
        <div>

        </div>
        <div style='padding:20px;background:#fff'>
            <el-input type='search' v-model='value' style='width:400px;float:right' suffix-icon='el-icon-search' @change='searchTable'>
            </el-input>
            <el-button type='primary' id='downBtn' @click='exportExcl()'>
                数据下载
            </el-button>
            <div style='clear:both'>

            </div>
            <el-table style='margin-top:20px' id='exportTable' :data='tableData'>
                <el-table-column prop='date' label='序号'></el-table-column>
                <el-table-column prop='name' label='用户ID'></el-table-column>
                <el-table-column prop='address' label='商品ID'></el-table-column>
                <el-table-column prop='' label='用户行为类型'></el-table-column>
                <el-table-column prop='' label='地理位置经度'></el-table-column>
                <el-table-column prop='' label='地理位置纬度'></el-table-column>
                <el-table-column prop='' label='商品类别ID'></el-table-column>
                <el-table-column prop='' label='记录时间'></el-table-column>
            </el-table>
        </div>
        
    </div>
</template>
<script>
    import {mapState} from 'vuex'
    import FileSaver from "file-saver";
    import XLSX from "xlsx";
    export default{
        data () {
            return {
                value: '',
                tableData: [{
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄'
                }, {
                    date: '2016-05-04',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1517 弄'
                }, {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1519 弄'
                }, {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1516 弄'
                }]
            }
        },
        methods:{
            searchTable () {
                this.$store.commit('')
                this.$store.dispatch()
            },
            exportExcl () {
                //blob URL形式文件下载
                /* 从表生成工作簿对象 */
                var wb = XLSX.utils.table_to_book(document.querySelector("#exportTable"));
                /* 获取二进制字符串作为输出 */
                var wbout = XLSX.write(wb, {
                    bookType: "xlsx",
                    bookSST: true,
                    type: "array"
                });
                try {
                    FileSaver.saveAs(
                    //Blob 对象表示一个不可变、原始数据的类文件对象。
                    //Blob 表示的不一定是JavaScript原生格式的数据。
                    //File 接口基于Blob，继承了 blob 的功能并将其扩展使其支持用户系统上的文件。
                    //返回一个新创建的 Blob 对象，其内容由参数中给定的数组串联组成。
                    new Blob([wbout], { type: "application/octet-stream" }),
                    //设置导出文件名称
                    "sheetjs.xlsx"
                    );
                } catch (e) {
                    if (typeof console !== "undefined") console.log(e, wbout);
                }
                return wbout;
            }
        }
    }
</script>
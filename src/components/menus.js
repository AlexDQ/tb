const menus = [
    {
        text: '全国消费用户位置分析',
        path: '/locationAnalysis',
        group_id: 'locationAnalysis'
    },
    {
        text: '销售数据分析',
        path: '/dataAnalysis',
        group_id: 'dataAnalysis'
    },
    {
        text: '用户行为习惯分析',
        path: '/behaviorAnalysis',
        group_id: 'behaviorAnalysis'
    },
    {
        text: '用户管理',
        path: '/userManagement',
        group_id: 'userManagement'
    },
    {
        text: '数据恢复',
        path: '/',
        group_id: 'dataRepair',
        children:[
            {
                text: '用户恢复',
                path: '/userRepair',
                group_id: 'userRepair'
            },
            {
                text: '销售数据恢复',
                path: '/salesRepair',
                group_id: 'salesRepair'
            }
        ]
    },
    {
        text: '销售数据管理',
        path: '/dataManagement',
        group_id: 'dataManagement'
    },
    {
        text: '用户行为类型管理',
        path: '/typeManagement',
        group_id: 'typeManagement'
    },
]
export default menus
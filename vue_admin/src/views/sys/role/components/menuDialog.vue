<script setup>


import {ref, defineProps, watch} from "vue";
import * as requestUtil from "@/util/request";
import {ElMessage} from "element-plus";

const form = ref({
  id: -1
})

// 默认参数
const defaultProps = {
  children: 'children',
  label: 'name',
}

const props = defineProps(
    {
      id: {
        required: true,
        type: Number,
        default: -1
      },
      menuDialogVisible: {
        required: true,
        type: Boolean,
        default: false
      }
    }
)

const treeRef = ref(null)

const formRef = ref(null)

const treeData = ref([])

const emits = defineEmits(["update:modelValue", "initRoleList"])

const initFormData = async (id) => {
  console.log('id:', id)
  const res = await requestUtil.get("menu/treeList?id=" + id)

  const res2 = await requestUtil.get("role/menus?id=" + id)

  treeData.value = res.data.treeList
  treeRef.value.setCheckedKeys(res2.data.menuIdList)
  form.value.id = id
}

watch(
    () => props.menuDialogVisible,
    () => {
      let id = props.id
      if (id !== -1) {
        initFormData(id)
      }
    }
)

const handleClose = () => {
  emits("update:modelValue", false)
}

const handleConfirm = async () => {
  let menuIdList = treeRef.value.getCheckedKeys()

  let result = await requestUtil.post("role/grant", {'id': form.value.id, 'menuIdList': menuIdList})
  let data = result.data
  if (data.code === 200) {
    ElMessage.success('执行成功')
    emits("initRoleList")
    handleClose()
  } else {
    ElMessage.error(data.msg)
  }
}


</script>

<template>
  <el-dialog
      model-value="menuDialogVisible"
      title="分配权限"
      width="30%"
      @close="handleClose"
  >

    <el-form
        ref="formRef"
        :model="form"
        label-width="100px"
    >

      <el-tree
          ref="treeRef"
          :data="treeData"
          :props="defaultProps"
          show-checkbox
          :default-expand-all=true
          node-key="id"
          :check-strictly=true
      />

    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="handleConfirm">确认</el-button>
        <el-button @click="handleClose">取消</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">

</style>
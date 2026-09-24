<!-- components/modals/EditBoardModal.vue -->
<template>
  <BaseModal v-model="isOpen" title="Настройки доски" width="500px">
    <form @submit.prevent="handleSave" class="board-form">
      <div class="form-group">
        <label>Название доски</label>
        <input
          v-model="form.name"
          class="input-field"
          required
          placeholder="Например: Разработка Kanban"
        />
      </div>

      <div class="form-group">
        <label>Описание</label>
        <textarea
          v-model="form.description"
          class="input-field textarea"
          rows="4"
          placeholder="Цели и задачи проекта..."
        ></textarea>
      </div>
    </form>

    <template #footer>
      <button type="button" class="btn btn-secondary" @click="isOpen = false">Отмена</button>
      <button type="button" class="btn btn-primary" @click="handleSave">Сохранить</button>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'

interface BoardData {
  id: number
  name: string
  description: string | null
}

const props = defineProps<{
  modelValue: boolean
  board?: BoardData | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: BoardData]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const form = ref<BoardData>({
  id: 0,
  name: '',
  description: '',
})

watch(
  () => props.board,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
    }
  },
  { immediate: true },
)

const handleSave = () => {
  emit('save', { ...form.value })
  isOpen.value = false
}
</script>

<style scoped>
.board-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #4a5568;
}
.input-field {
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.input-field:focus {
  border-color: #168be5;
}
.textarea {
  resize: vertical;
  font-family: inherit;
}
.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  font-weight: 500;
}
.btn-primary {
  background: #168be5;
  color: white;
}
.btn-secondary {
  background: #edf2f7;
  color: #4a5568;
}
</style>

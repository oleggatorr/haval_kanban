<!-- components/modals/EditSubtaskModal.vue -->
<template>
  <BaseModal v-model="isOpen" title="Редактирование подзадачи" width="500px">
    <form @submit.prevent="handleSave" class="subtask-form">
      <div class="form-group">
        <label>Название</label>
        <input
          v-model="form.name"
          class="input-field"
          required
          placeholder="Введите название подзадачи"
        />
      </div>

      <div class="form-group">
        <label>Описание</label>
        <textarea
          v-model="form.description"
          class="input-field textarea"
          rows="4"
          placeholder="Детали задачи..."
        ></textarea>
      </div>

      <div class="form-group">
        <label>Статус</label>
        <select v-model="form.status_id" class="input-field">
          <option :value="null">Не выбран</option>
          <option :value="1">В работе</option>
          <option :value="2">На проверке</option>
          <option :value="3">Завершено</option>
        </select>
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

interface SubtaskData {
  id: number
  name: string
  description: string | null
  status_id: number | null
}

const props = defineProps<{
  modelValue: boolean
  subtask?: SubtaskData | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: SubtaskData]
}>()

// Управление открытием через v-model
const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

// Локальная копия данных формы
const form = ref<SubtaskData>({
  id: 0,
  name: '',
  description: '',
  status_id: null,
})

// Заполняем форму данными при открытии модалки
watch(
  () => props.subtask,
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
.subtask-form {
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

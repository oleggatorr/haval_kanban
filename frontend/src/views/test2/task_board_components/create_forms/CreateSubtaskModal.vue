<!-- components/modals/CreateSubtaskModal.vue -->
<template>
  <BaseModal v-model="isOpen" title="Добавить подзадачу" width="500px">
    <form @submit.prevent="handleSave" class="subtask-form">
      <div class="form-group">
        <label>Название подзадачи</label>
        <input
          v-model="form.name"
          class="input-field"
          required
          placeholder="Например: Написать тесты"
          autofocus
        />
      </div>

      <div class="form-group">
        <label>Описание</label>
        <textarea
          v-model="form.description"
          class="input-field textarea"
          rows="3"
          placeholder="Детали подзадачи..."
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Дата начала</label>
          <input v-model="form.date_time_start" type="datetime-local" class="input-field" />
        </div>

        <div class="form-group">
          <label>Дата окончания</label>
          <input v-model="form.date_time_end" type="datetime-local" class="input-field" />
        </div>
      </div>
    </form>

    <template #footer>
      <button type="button" class="btn btn-secondary" @click="isOpen = false">Отмена</button>
      <button type="button" class="btn btn-primary" @click="handleSave">Создать</button>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'

interface SubtaskData {
  name: string
  description?: string | null
  date_time_start?: string | null
  date_time_end?: string | null
}

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: SubtaskData]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const form = ref<SubtaskData>({
  name: '',
  description: '',
  date_time_start: null,
  date_time_end: null,
})

// Сбрасываем форму при открытии модалки
watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal) {
      form.value = {
        name: '',
        description: '',
        date_time_start: null,
        date_time_end: null,
      }
    }
  },
)

const handleSave = () => {
  if (!form.value.name.trim()) return

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
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
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

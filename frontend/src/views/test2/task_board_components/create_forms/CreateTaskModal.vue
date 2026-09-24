<!-- components/modals/CreateTaskModal.vue -->
<template>
  <BaseModal v-model="isOpen" title="Создать задачу" width="500px">
    <form @submit.prevent="handleSave" class="task-form">
      <div class="form-group">
        <label>Название задачи</label>
        <input
          v-model="form.title"
          class="input-field"
          required
          placeholder="Например: Реализовать авторизацию"
          autofocus
        />
      </div>

      <div class="form-group">
        <label>Описание</label>
        <textarea
          v-model="form.description"
          class="input-field textarea"
          rows="4"
          placeholder="Подробное описание задачи..."
        ></textarea>
      </div>

      <div class="form-group">
        <label>Приоритет</label>
        <select v-model="form.priority" class="input-field">
          <option value="low">Низкий</option>
          <option value="medium">Средний</option>
          <option value="high">Высокий</option>
          <option value="urgent">Срочный</option>
        </select>
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

interface TaskData {
  title: string
  description?: string | null
  priority?: 'low' | 'medium' | 'high' | 'urgent'
}

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: TaskData]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const form = ref<TaskData>({
  title: '',
  description: '',
  priority: 'medium',
})

// Сбрасываем форму при открытии модалки
watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal) {
      form.value = {
        title: '',
        description: '',
        priority: 'medium',
      }
    }
  },
)

const handleSave = () => {
  if (!form.value.title.trim()) return

  emit('save', { ...form.value })
  isOpen.value = false
}
</script>

<style scoped>
.task-form {
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

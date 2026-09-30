<!-- components/modals/CreateTaskModal.vue -->
<template>
  <BaseModal
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="Создать задачу"
    width="500px"
  >
    <form @submit.prevent="handleSave" class="task-form">
      <div class="form-group">
        <label>Название задачи</label>
        <input
          v-model="form.name"
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
    </form>

    <template #footer>
      <button type="button" class="btn btn-secondary" @click="$emit('update:modelValue', false)">
        Отмена
      </button>
      <button type="submit" class="btn btn-primary">Создать</button>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'

interface TaskFormData {
  name: string
  description?: string | null
}

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: TaskFormData]
}>()

const form = ref<TaskFormData>({ name: '', description: '' })

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal) form.value = { name: '', description: '' }
  },
)

const handleSave = () => {
  if (!form.value.name.trim()) return

  console.log('[Modal] Emitting save:', form.value) // Проверка в консоли
  emit('save', {
    name: form.value.name.trim(),
    description: form.value.description?.trim() || null,
  })

  emit('update:modelValue', false) // Закрываем окно
}
</script>

<!-- components/modals/EditColumnModal.vue -->
<template>
  <BaseModal
    v-model="isOpen"
    :title="isEditMode ? 'Редактирование колонки' : 'Новая колонка'"
    width="400px"
  >
    <form @submit.prevent="handleSave" class="column-form">
      <div class="form-group">
        <label>Название колонки</label>
        <input
          v-model="form.name"
          class="input-field"
          required
          placeholder="Например: В работе"
          autofocus
        />
      </div>

      <div class="form-group">
        <label>Описание (опционально)</label>
        <textarea
          v-model="form.description"
          class="input-field textarea"
          rows="3"
          placeholder="Краткое описание этапа..."
        ></textarea>
      </div>

      <!-- Можно добавить выбор цвета, если нужно -->
      <div class="form-group">
        <label>Цвет маркера</label>
        <div class="color-picker">
          <span
            v-for="color in colors"
            :key="color"
            class="color-dot"
            :style="{ background: color }"
            :class="{ active: form.color === color }"
            @click="form.color = color"
          ></span>
        </div>
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

interface ColumnData {
  id?: number
  name: string
  description: string | null
  color?: string // Если вы решите хранить цвет в БД
}

const props = defineProps<{
  modelValue: boolean
  column?: ColumnData | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  save: [data: ColumnData]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const isEditMode = computed(() => !!props.column?.id)

const colors = ['#168be5', '#ff9f43', '#2ecc71', '#9b59b6', '#e74c3c', '#34495e']

const form = ref<ColumnData>({
  name: '',
  description: '',
  color: '#168be5',
})

watch(
  () => props.column,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
    } else {
      // Сброс формы для режима создания
      form.value = { name: '', description: '', color: colors[0] }
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
.column-form {
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

.color-picker {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}
.color-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: transform 0.2s;
}
.color-dot:hover {
  transform: scale(1.1);
}
.color-dot.active {
  border-color: #2d3748;
  box-shadow: 0 0 0 2px white inset;
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

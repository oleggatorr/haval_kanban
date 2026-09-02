<!-- src/components/common/AppTextarea.vue -->
<template>
  <div class="app-textarea-wrapper">
    <!-- Лейбл, если он передан -->
    <label v-if="label" :for="id" class="app-textarea__label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>

    <textarea
      :id="id"
      :value="modelValue"
      :placeholder="placeholder"
      :rows="rows"
      :disabled="disabled"
      :class="{ 'has-error': error }"
      @input="onInput"
      class="app-textarea"
    ></textarea>

    <!-- Сообщение об ошибке -->
    <span v-if="error" class="app-textarea__error">{{ error }}</span>

    <!-- Счетчик символов (опционально) -->
    <span v-if="maxlength && modelValue" class="app-textarea__counter">
      {{ modelValue.length }} / {{ maxlength }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { useAttrs } from 'vue'

const props = defineProps<{
  modelValue: string
  label?: string
  placeholder?: string
  rows?: number | string
  disabled?: boolean
  error?: string
  required?: boolean
  maxlength?: number
  id?: string // Уникальный ID для связки label и textarea
}>()

const emit = defineEmits(['update:modelValue'])

// Генерируем ID, если он не передан, чтобы label работал корректно
const attrs = useAttrs()
const uniqueId = props.id || `textarea-${Math.random().toString(36).substr(2, 9)}`

const onInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement
  emit('update:modelValue', target.value)
}
</script>

<style scoped>
.app-textarea-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
  position: relative;
}

.app-textarea__label {
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.required {
  color: #ff4d4f;
  margin-left: 4px;
}

.app-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical; /* Разрешаем менять размер только по вертикали */
  transition: border-color 0.2s;
  min-height: 80px;
}

.app-textarea:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.app-textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #999;
}

.has-error {
  border-color: #ff4d4f !important;
}

.has-error:focus {
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.2) !important;
}

.app-textarea__error {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
}

.app-textarea__counter {
  position: absolute;
  bottom: -20px;
  right: 0;
  font-size: 12px;
  color: #999;
}
</style>

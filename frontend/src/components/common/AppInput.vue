<!-- src/components/common/AppInput.vue -->
<template>
  <div class="app-input-wrapper">
    <!-- Лейбл -->
    <label v-if="label" :for="inputId" class="app-input__label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>

    <div class="app-input__container">
      <!-- Иконка слева (опционально) -->
      <span v-if="$slots.prefix" class="app-input__prefix">
        <slot name="prefix"></slot>
      </span>

      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :autocomplete="autocomplete"
        :class="{ 'has-error': error, 'has-prefix': $slots.prefix }"
        @input="onInput"
        class="app-input"
      />

      <!-- Иконка справа (например, глаз для пароля) -->
      <span v-if="$slots.suffix" class="app-input__suffix">
        <slot name="suffix"></slot>
      </span>
    </div>

    <!-- Сообщение об ошибке -->
    <span v-if="error" class="app-input__error">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string | number
  label?: string
  type?: string
  placeholder?: string
  disabled?: boolean
  error?: string
  required?: boolean
  autocomplete?: string
  id?: string
}>()

const emit = defineEmits(['update:modelValue'])

// Генерируем ID для связки label и input
const inputId = props.id || `input-${Math.random().toString(36).substr(2, 9)}`

const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<style scoped>
.app-input-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
  position: relative;
}

.app-input__label {
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.required {
  color: #ff4d4f;
  margin-left: 4px;
}

.app-input__container {
  position: relative;
  display: flex;
  align-items: center;
}

.app-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.2s;
  background-color: #fff;
}

/* Отступы для иконок */
.has-prefix {
  padding-left: 35px;
}

.app-input__prefix,
.app-input__suffix {
  position: absolute;
  color: #999;
  display: flex;
  align-items: center;
  pointer-events: none; /* Чтобы клик проходил сквозь иконку в инпут */
}

.app-input__prefix {
  left: 10px;
}

.app-input__suffix {
  right: 10px;
  pointer-events: auto; /* Для кнопки "показать пароль" кликабельность нужна */
}

.app-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.app-input:disabled {
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

.app-input__error {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
}
</style>

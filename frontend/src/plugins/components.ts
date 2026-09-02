// src/plugins/components.ts
import type { App } from 'vue'
import AppButton from '@/components/common/AppButton.vue'
import AppTextarea from '@/components/common/AppTextarea.vue'
import AppInput from '@/components/common/AppInput.vue'
// import AppModal from '@/components/common/AppModal.vue'

// Список всех компонентов, которые хотим зарегистрировать глобально
const globalComponents = {
  AppButton,
  AppTextarea,
  AppInput,
  //   AppModal,
}

export function registerGlobalComponents(app: App<Element>) {
  // Регистрируем каждый компонент
  Object.entries(globalComponents).forEach(([name, component]) => {
    app.component(name, component)
  })
}

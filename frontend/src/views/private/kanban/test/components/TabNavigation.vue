<template>
  <nav class="tabs">
    <button
      v-for="tab in tabs"
      :key="tab.name"
      :class="['tab', { active: activeTab === tab.name }]"
      @click="$emit('change-tab', tab.name)"
      @mousedown="handleTabPress"
      @mouseup="handleTabRelease"
      @mouseleave="handleTabRelease"
    >
      <svg viewBox="0 0 24 24" v-html="tab.icon"></svg>
      {{ tab.label }}
    </button>
  </nav>
</template>

<script setup>
defineProps({
  tabs: {
    type: Array,
    required: true,
  },
  activeTab: {
    type: String,
    default: 'board',
  },
})

defineEmits(['change-tab'])

const handleTabPress = (e) => {
  e.target.classList.add('is-pressed')
}

const handleTabRelease = (e) => {
  e.target.classList.remove('is-pressed')
}
</script>

<style scoped>
.tabs {
  height: 100%;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tab {
  height: 48px;
  border: 0;
  border-radius: 13px;
  padding: 0 19px;
  display: flex;
  align-items: center;
  gap: 9px;
  color: rgba(255, 255, 255, 0.78);
  background: transparent;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.tab::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  transform: translate(-50%, -50%);
  transition:
    width 0.35s,
    height 0.35s;
  pointer-events: none;
}

.tab:active::before {
  width: 180px;
  height: 180px;
}

.tab:hover:not(.active) {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.95);
}

.tab svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  transition: transform 0.2s ease;
}

.tab:hover svg {
  transform: scale(1.1);
}

.tab.active {
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.17);
}

/* Уменьшенный эффект клика для вкладок */
.tab:active,
.tab.is-pressed {
  transform: scale(0.98);
  background: rgba(255, 255, 255, 0.18);
}
</style>

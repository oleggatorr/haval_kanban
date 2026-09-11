<template>
  <article class="task-card">
    <div class="task-top">
      <h3>{{ title }}</h3>

      <button class="card-button">
        <svg viewBox="0 0 24 24">
          <path d="M6 4h12v16H6z" />
          <path d="M9 9h6M9 13h6" />
        </svg>
      </button>
    </div>

    <span :class="['tag', tagClass]">
      {{ tag }}
    </span>

    <div class="task-meta">
      <span class="meta-item">
        <span class="meta-icon comment"></span>
        {{ comments }}
      </span>

      <span class="meta-item">
        <span class="meta-icon subtask"></span>
        {{ subtasks }}
      </span>

      <span v-if="done" class="done-icon"> ✓ </span>
    </div>
  </article>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },

  tag: {
    type: String,
    default: 'Задача',
  },

  tagClass: {
    type: String,
    default: 'purple',
  },

  comments: {
    type: [String, Number],
    default: 0,
  },

  subtasks: {
    type: [String, Number],
    default: 0,
  },

  done: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.task-card {
  border-radius: 15px;

  padding: 16px;

  background: linear-gradient(135deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.07));

  border: 1px solid rgba(255, 255, 255, 0.22);

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 8px 25px rgba(20, 25, 60, 0.08);

  min-height: 137px;
}

.task-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.task-card h3 {
  margin: 0 0 14px;

  font-size: 14px;
  line-height: 1.35;

  font-weight: 500;
}

.card-button {
  width: 24px;
  height: 24px;

  padding: 0;

  border: 0;
  background: transparent;

  color: rgba(255, 255, 255, 0.72);
}

.card-button svg {
  width: 18px;
  height: 18px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
}

.tag {
  display: inline-flex;
  align-items: center;

  height: 24px;
  padding: 0 9px;

  border-radius: 7px;

  font-size: 11px;
  font-weight: 500;
}

.tag.purple {
  background: rgba(139, 119, 255, 0.65);
}

.tag.pink {
  background: rgba(184, 102, 221, 0.65);
}

.tag.blue {
  background: rgba(76, 178, 224, 0.65);
}

.tag.green {
  background: rgba(85, 175, 119, 0.65);
}

.tag.orange {
  background: rgba(194, 139, 85, 0.7);
}

.task-meta {
  display: flex;
  align-items: center;

  gap: 15px;

  margin-top: 17px;

  color: rgba(255, 255, 255, 0.72);

  font-size: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.meta-icon {
  width: 15px;
  height: 15px;

  border: 1.4px solid currentColor;
  display: inline-block;
}

.meta-icon.comment {
  border-radius: 50%;
}

.meta-icon.subtask {
  border-radius: 4px;
}

.done-icon {
  margin-left: auto;

  width: 21px;
  height: 21px;

  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 12px;
}
</style>

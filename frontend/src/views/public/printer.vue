<!-- src/components/ProjectInfoCard.vue -->
<script setup lang="ts">
import { toRef } from 'vue'
import { useProjectInfo } from '@/composables/taskboard/useTaskBoardInfo'
import { useTaskBoard } from '@/composables/taskboard/useTaskBoard'

const props = defineProps<{
  projectId: number | string
}>()

const projectIdRef = toRef(props, 'projectId')

// --- Информация о проекте ---
const { project, members, statuses, projectName, isLoaded, loading, error } =
  useProjectInfo(projectIdRef)

// --- Доска проекта ---
const {
  board,
  columns,
  tasks,
  subtasks,
  isLoaded: isBoardLoaded,
  loading: boardLoading,
  error: boardError,
  getTasksByColumn,
  getSubtasksByTask,
} = useTaskBoard(projectIdRef)
</script>

<template>
  <div class="project-info-card">
    <div v-if="loading && !isLoaded">Загрузка…</div>

    <div v-else-if="error">Ошибка: {{ error.message ?? error }}</div>

    <template v-else-if="isLoaded && project">
      <h2>{{ projectName }} (#{{ project.id }})</h2>

      <!-- === Основные поля проекта === -->
      <section>
        <h3>Основное</h3>
        <ul>
          <li><b>id:</b> {{ project.id }}</li>
          <li><b>name:</b> {{ project.name }}</li>
          <li><b>create_at:</b> {{ project.create_at }}</li>
          <li><b>update_at:</b> {{ project.update_at ?? '—' }}</li>
          <li><b>is_active:</b> {{ project.is_active }}</li>
          <li><b>remove_at:</b> {{ project.remove_at ?? '—' }}</li>
        </ul>
      </section>

      <!-- === Вложенный объект data === -->
      <section v-if="project.data">
        <h3>data</h3>
        <ul>
          <li><b>id:</b> {{ project.data.id }}</li>
          <li><b>project_id:</b> {{ project.data.project_id }}</li>
          <li><b>big_description:</b> {{ project.data.big_description }}</li>
          <li><b>create_at:</b> {{ project.data.create_at }}</li>
          <li><b>update_at:</b> {{ project.data.update_at ?? '—' }}</li>
          <li><b>is_active:</b> {{ project.data.is_active }}</li>
          <li><b>remove_at:</b> {{ project.data.remove_at ?? '—' }}</li>
        </ul>
      </section>

      <!-- === Участники === -->
      <section>
        <h3>Участники ({{ members.length }})</h3>
        <ul v-if="members.length">
          <li v-for="member in members" :key="member.id">
            <b>id:</b> {{ member.id }} — <b>username:</b> {{ member.username }} — <b>email:</b>
            {{ member.email }}
          </li>
        </ul>
        <p v-else>Нет участников</p>
      </section>

      <!-- === Статусы === -->
      <section>
        <h3>Статусы ({{ statuses.length }})</h3>
        <ul v-if="statuses.length">
          <li v-for="status in statuses" :key="status.id">
            <b>id:</b> {{ status.id }} — <b>name:</b> {{ status.name }} — <b>color:</b>
            {{ status.color ?? '—' }} {{ status.description ?? '—' }}
          </li>
        </ul>
        <p v-else>Нет статусов</p>
      </section>

      <hr />

      <!-- === Доска === -->
      <section>
        <h3>Доска</h3>

        <div v-if="boardLoading && !isBoardLoaded">Загрузка доски…</div>
        <div v-else-if="boardError">Ошибка доски: {{ boardError.message ?? boardError }}</div>

        <template v-else-if="isBoardLoaded && board">
          <p><b>board.id:</b> {{ board.id }} — <b>board.name:</b> {{ board.name }}</p>

          <div v-for="column in columns" :key="column.id" class="column">
            <h4>{{ column.name }} (#{{ column.id }})</h4>

            <ul v-if="getTasksByColumn(column.id).length">
              <li v-for="task in getTasksByColumn(column.id)" :key="task.id">
                <b>task.id:</b> {{ task.id }} — <b>name:</b> {{ task.name }} — <b>position:</b>
                {{ task.position }} —
                <b>completed:</b>
                {{ task.completed_subtasks_count ?? 0 }}/{{ getSubtasksByTask(task.id).length }}

                <ul v-if="getSubtasksByTask(task.id).length">
                  <li v-for="sub in getSubtasksByTask(task.id)" :key="sub.id">
                    <b>subtask.id:</b> {{ sub.id }} — <b>name:</b> {{ sub.name }} —
                    <b>status_id:</b> {{ sub.status_id }} — <b>end:</b>
                    {{ sub.date_time_end ?? '—' }}
                  </li>
                </ul>
              </li>
            </ul>
            <p v-else>Задач нет</p>
          </div>
        </template>

        <p v-else>Доска не найдена</p>
      </section>
    </template>

    <div v-else>Проект не найден</div>
  </div>
</template>

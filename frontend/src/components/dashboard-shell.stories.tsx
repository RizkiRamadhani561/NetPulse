import type { Meta, StoryObj } from "@storybook/nextjs-vite";

import { DashboardShell } from "./dashboard-shell";

const meta = {
  title: "Foundation/Dashboard Shell",
  component: DashboardShell,
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof DashboardShell>;

export default meta;
type Story = StoryObj<typeof meta>;

export const IndonesianPreview: Story = {};

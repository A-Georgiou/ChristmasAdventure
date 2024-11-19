import api from './axiosConfig';

export const storyApi = {
  continueStory: async (storyData) => {
    try {
      const response = await api.post('/continue_story', {
        story_so_far: storyData.currentStory,
        choice: storyData.choice,
        node_count: storyData.nodeCount
      });
      return response.data;
    } catch (error) {
      console.error('Story API Error:', error);
      throw error;
    }
  }
};
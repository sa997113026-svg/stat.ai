// Training videos shown on /videos.
//
// HOW TO ADD A VIDEO: paste a link into `url`. Supported:
//   - YouTube:  https://www.youtube.com/watch?v=XXXXXXXXXXX  or  https://youtu.be/XXXXXXXXXXX
//   - Local file: put the .mp4 in StatSaksham-AI/public/videos/ and use  '/videos/my-video.mp4'
//   - Any direct .mp4 / .webm link
// Entries with an empty url are shown as "link not added yet" (they never show a broken player).
export type TrainingVideo = {
  id: string;
  title: string;
  competency: string;
  duration: string;
  url: string;
};

export const videos: TrainingVideo[] = [
  { id: 'vid-sampling', title: 'Sampling Methods for Household Surveys', competency: 'Sampling Methods', duration: '', url: '' },
  { id: 'vid-python', title: 'Python for Statistical Computing', competency: 'Python for Statistical Computing', duration: '', url: '' },
  { id: 'vid-dataviz', title: 'Data Visualization for Official Statistics', competency: 'Data Visualization', duration: '', url: '' },
  { id: 'vid-lfs', title: 'Labour Force Survey Frameworks', competency: 'Labour Force Frameworks', duration: '', url: '' },
];

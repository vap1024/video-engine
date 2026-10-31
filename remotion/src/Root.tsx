import React from 'react';
import {Composition} from 'remotion';
import {TitleCard, EndCard, LowerThird} from './Cards';

export const Root: React.FC = () => (
  <>
    <Composition id="TitleCard" component={TitleCard} durationInFrames={150} fps={30} width={1280} height={720} />
    <Composition id="EndCard" component={EndCard} durationInFrames={240} fps={30} width={1280} height={720} />
    <Composition
      id="LowerThird"
      component={LowerThird}
      durationInFrames={30}
      fps={30}
      width={1280}
      height={720}
      defaultProps={{name: 'БАРСИК', role: 'CEO · ОХОТНИК · СПИТ 16 ЧАСОВ', color: '#e8873a'}}
    />
  </>
);
